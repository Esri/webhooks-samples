from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import unquote
import requests
import time
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ExtractChangesMGR:

    def __init__(self, url, portalContext, serverContext, username, password, arcgis=False):
        self.url = url
        self.portalContext = portalContext
        self.serverContext = serverContext
        self.username = username
        self.password = password
        self.arcgis = arcgis
        self.common_headers = {}
        self.common_query_parameters = {"f": "json"}
        self.token = None
        self.token = self._get_token(url, username, password) if not arcgis else None
        if self.token:
            self.common_query_parameters.update({"token":self.token})

    def _get_token(self, url, username, password):

        if not self.arcgis:
            token_url = "{}/{}/sharing/rest/generateToken".format(url, self.serverContext)
            portal_url = "{}/{}/sharing/rest/generateToken".format(url, self.portalContext)
        else:
            token_url = "{}/sharing/rest/generateToken".format(url)
            portal_url = "{}/sharing/rest/generateToken".format(url)

        
        # Token URL in a portal can have redirects
        try:
            token_response = requests.get(token_url, verify=True, allow_redirects=True)
        except Exception as e:
            raise Exception
        
        token_url = token_response.url

        token_referrer = portal_url
        token_params = {
            "username": username,
            "password": password,
            "client": "referer",
            "referer": token_referrer,
            "expiration": 1440,  # 24 hour token
            "f": "json",
        }
        try:
            return self._make_request(portal_url, token_params)['token']
        except Exception as e:
            print("Failed to get a portal token: \n   {}".format(e))


    def _make_request(self, u, query_parameters=None, headers=None, timeout=None, files=None):
        """Make a POST HTTP request and return the JSON response."""
        
        if not query_parameters:
            query_parameters = {}
        if not headers:
            headers = {}

        # Add token and f=pjson to query parameters
        query_parameters.update(self.common_query_parameters)
        
        # Convert any lists or dicts in query parameters to string so that requests.post can correctly pass them when
        # making REST API call.
        post_data = {}
        for param_name, param_value in query_parameters.items():
            if isinstance(param_value, (dict, list)):
                post_data[param_name] = json.dumps(param_value)
            else:
                post_data[param_name] = param_value

        # Add referrer to the headers
        headers.update(self.common_headers)

        if u:
            try:
                response = requests.post(u, data=post_data, headers=headers, timeout=timeout, files=files, verify=False)
                if response.status_code == 200:
                    response_json = response.json()
                else:                    
                    raise HTTPError(u, response.status_code, response.reason)
            except Exception as e:
                print("ERROR: \n{}".format(e))
                raise

        
            if "error" in response_json or ("status" in response_json and response_json["status"] == "error"):    
                error_reason = []
                for key in ("reason", "messages"):
                    if key in response_json:
                        value = response_json[key]
                        if isinstance(value, list):
                            error_reason.append(", ".join(value))
                        else:
                            error_reason.append(value)
                print(error_reason)
            
            return response_json


    def parseResults(self, resultJSONURL):

        resultJSON = self._make_request(resultJSONURL)
        
        if "edits" in resultJSON:
            print("Found  {}  edits in the changes file".format(len(resultJSON['edits'])))
        else:
            print("No edits found")

        return resultJSON


    def waitForStauts(self, statusURL):

        statusPayload = {"status":"foo"}
        counter = 0
        
        while statusPayload["status"].upper() != "COMPLETED":
            statusPayload = self._make_request(statusURL)
            counter += 1
            time.sleep(1)
            if counter == 20:
                print("No results after 20 seconds, something is probably wrong")
                continue
        
        try:
            return statusPayload['resultUrl']
        except Exception:
            print("Failed to get a resultURL")


    def getExtractChanges(self, changesURL):
        
        # Depending on the type of changes happening in your feature service,
        #  the following parameters can be updated to get back specific types
        #  of changes. Below is set to return any Insert, Update or Delete
        if not self.arcgis:
            parse = urlparse(changesURL)
            extract_params = {
                #"token": self.token,
                "serverGens": parse_qs(parse.query)['serverGens'][0],
                "returnInserts": "true",
                "returnUpdates": "true",
                "returnDeletes": "true",
                "returnAttachments": "false",
                "returnAttachmentsDataByUrl": "false"
            }
            if self.token:
                headers = {"token":self.token}
            else:
                headers = {}
            changePayload = self._make_request(changesURL.split("?")[0], extract_params, headers)
        else:
            noquote = unquote(changesURL)
            changePayload = self._make_request(noquote)

        if "statusUrl" in changePayload:
            return changePayload['statusUrl']
        else:
            print("No status URL found, cannot proceed")


    def doExtractChanges(self, changesURL):

        statusURL = self.getExtractChanges(changesURL)

        resultJSONURL = self.waitForStauts(statusURL)

        changeResults = self.parseResults(resultJSONURL)

        return changeResults

''' __main__ used to run this as a stand alone script.
	When used in a larger webhook workflow, this script would be imported and the 
	ExtractChangesMGR object would be used.
'''
if __name__ == "__main__":

	url = "https://www.server.com/"
	pContext = "portal"
	sContext = "server"
	username = "admin"
	pword = "password"

	changeURL = "https://www.server.com/server/rest/services/ServiceName/FeatureServer/extractChanges?serverGens=%5B1730385704442,1730385704443%5D"

	ec = ExtractChangesMGR(url, pContext, sContext, username, pword)

	changes = ec.doExtractChanges(changeURL)
	if changes:
		if "edits" in changes:
			for e in changes['edits']:
				print(e)
		else:
			print("No edits found in response")
				