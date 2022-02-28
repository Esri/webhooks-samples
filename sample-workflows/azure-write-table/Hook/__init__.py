import logging
import json
import datetime
import uuid
import re
import urllib.parse
import azure.functions as func

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
import hash_check

appJSON ="application/json"

def main(req: func.HttpRequest,  outputTable: func.Out[str]) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')
    logging.info("Method type: {}".format(req.method))
    logging.info("params: {}".format(req.params))
    headersAsDict = dict(req.headers)
    logging.info(json.dumps(headersAsDict, indent=2))
    try:
        logging.info("body: {}".format(req.get_json()))
    except:
        logging.info("body is no json")
    try:
        logging.info("body: {}".format(req.get_body()))
    except:
        logging.info("body is no json")


    """ A webhook request is generally made via POST.
    The ArcGIS Online Feature Service webhook will make a GET request when using the signatureKey as the 
    first step in the CRC. Logic below will check if a 'crc_token' is included in the request and
    attempt to generate the proper response based on a known secret key.
    """
    if req.method == "GET":
        data ={
            "PartitionKey": "AGOL",
            "RowKey": str(uuid.uuid4()),
            "Timestamp": str(datetime.datetime.now()),            
            "sigKey": "CREATEHOOK"
        }

        if req.params:
            try:
                data["payload"] = json.dumps(str(req.params))
            except Exception as e:
                errMsg = "GET: No REQ params: {}".format(e)
                logging.info(errMsg)

        try:
            crc = req.params.get('crc_token')
            if crc:
                signature = hash_check.crc_response(crc)

                logging.info("HASHKEY: {}".format(signature))

                data["hashKey"] = signature
                outputTable.set(json.dumps(data))

                return func.HttpResponse(
                    json.dumps({"response_token": signature}),
                    status_code=200
                )
        except Exception as e:
            errMsg = "Failed to properly answer the CRC req: {}".format(e)
            logging.info(errMsg)
            return func.HttpResponse(json.dumps({'success':False, 'message': errMsg}),
                mimetype=appJSON,
                status_code=400
            )

        return func.HttpResponse(json.dumps({'success':True}),
                mimetype=appJSON,
                status_code=200
        )

    """ Webhook calls are generally POSTed
    """
    if req.method == "POST":
        try:
            msgBody = req.get_body()
            logging.info("msgbody from POST: {}".format(msgBody))

            # Feature Service Specific Payload logic
            try:
                payload = re.split(b'payload=|&', msgBody)[1]
                logging.info("Payload from POST: {}".format(payload))
                jLoad = json.loads(payload)

                v = None
                xsig = None
                try:
                    hashKey = re.split(b'x-esriHook-Signature=|&', msgBody)[2]
                    xsig = urllib.parse.unquote(hashKey.decode('UTF-8')) or ""
                    if xsig:
                        v = hash_check.verify(payload, xsig)
                except:
                    logging.info("FS signatureKey not found >> msg not secured")
                
                i = 0
                while i < len(jLoad):
                    data = {
                        "PartitionKey": "AGOL",
                        "RowKey": str(uuid.uuid4()),
                        "Timestamp": str(datetime.datetime.now()),
                        "payload": json.dumps(jLoad[i]),
                        "serviceName": jLoad[i]['serviceName'],
                        "hashKey": xsig,
                        "hookName": jLoad[i]['name'],
                        "verified": v
                    } 
                    logging.info("Data to push into storage: {}".format(data))

                    try:
                        outputTable.set(json.dumps(data))

                    except Exception as e:
                        errMsg = "Failed to create Feature Service webhook record: {}".format(e)
                        logging.info(errMsg)
                        return func.HttpResponse(json.dumps({'success':False, 'message': errMsg}),
                            mimetype=appJSON,
                            status_code=400
                        )

                    i += 1

            # Portal webhooks deliver content as single JSON object
            except:
                logging.info("Portal webhook: {}".format(msgBody))
                data = {"PartitionKey": "PortalHook",
                        "RowKey": str(uuid.uuid4()),
                        "Timestamp": str(datetime.datetime.now()),
                        "payload": msgBody,
                        "serviceName": msgBody['info']['portalURL'],
                        "hashKey": None,
                        "hookName": msgBody['info']['webhookName'],
                        "verified": None
                }
                try:
                    outputTable.set(json.dumps(data))

                except Exception as e:
                    errMsg = "Failed to create Portal webhook record: {}".format(e)
                    logging.info(errMsg)
                    return func.HttpResponse(json.dumps({'success':False, 'message': errMsg}),
                        mimetype=appJSON,
                        status_code=400
                    )


            logging.info("Pushed the record successfully")
            return func.HttpResponse(json.dumps({'success':True}),
                mimetype=appJSON,
                status_code=200
            )

        except Exception as e:
            errMsg = "Failed to handle hook message: {}".format(e)
            logging.info(errMsg)
            return func.HttpResponse(json.dumps({'success':False, 'message': errMsg}),
                mimetype=appJSON,
                status_code=400
            )
