"""  Copyright 2021 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """

import logging
import json
import re
import urllib.parse
import azure.functions as func

import os, sys
# Required to import modules in Azure
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
import hash_check

appJSON ="application/json"


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')
    logging.info("Method type: {}".format(req.method))
    logging.info("Params: {}".format(req.params))
    headersAsDict = dict(req.headers)
    logging.info("Headers: {}".format(json.dumps(headersAsDict, indent=2)))
    
    try:
        logging.info("JSON: {}".format(req.get_json()))
    except:
        pass
    try:
        logging.info("Body: {}".format(req.get_body()))
    except:
        pass


    """ A webhook request is generally made via POST.
    The ArcGIS Online Feature Service webhook will make a GET request when using the signatureKey as the 
    first step in the CRC. Logic below will check if a 'crc_token' is included in the request and
    attempt to generate the proper response based on a known secret key.
    """
    if req.method == "GET":
        if req.params:
            try:
                logging.info(json.dumps(str(req.params)))
            except Exception as e:
                errMsg = "GET: No REQ params: {}".format(e)
                logging.info(errMsg)

        try:
            crc = req.params.get('crc_token')
            if crc:
                signature = hash_check.crc_response(crc)
                logging.info("CRC Response:: {}".format(signature))

                # CRC expects the response as 'response_token':'token'
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
            logging.info("msgbody in POST: {}".format(msgBody))
            
            # Feature Service Specific Payload logic
            try:                
                payload = re.split(b'payload=|&', msgBody)[1]
                logging.info("Payload in POST: {}".format(payload)) 
                jLoad = json.loads(payload)
                i = 0
                while i < len(jLoad):
                    logging.info("Individual FS payload ({}): {}".format(i, jLoad[i]))
                    i += 1

                # Check if FS has returned a sigatureKey
                try:
                    hashKey = re.split(b'x-esriHook-Signature=|&', msgBody)[2]
                    xsig = urllib.parse.unquote(hashKey.decode('UTF-8')) or ""
                    if xsig:
                        v = True if hash_check.verify(payload, xsig) else False
                        logging.info("The payload has been confirmed: {}".format(v))
                except:
                    pass  

            # Portal webhooks deliver content as single JSON object
            except:
                logging.info("Portal webhook: {}".format(msgBody))          
        

            # Finished - respond to the calling application with 200  
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