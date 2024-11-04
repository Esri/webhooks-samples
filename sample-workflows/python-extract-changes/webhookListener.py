"""  Copyright 2024 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """

from flask import Flask, request
from OpenSSL import SSL
import ec


# Login information for the Enterprise to reach back and call extract changes
url = "https://www.server.com/"
pContext = "portal"
sContext = "server"
username = "admin"
pword = "password"

app = Flask(__name__)

ecMgr = ec.ExtractChangesMGR(url, pContext, sContext, username, pword)

@app.route('/', methods=['POST','GET'])
def index():
	if request.method == 'GET':
		return '<h1>Hello from Webhook Listener!</h1>'

	if request.method == 'POST':		
		# Get the payload
		req_data = request.get_json()
		if "changesUrl" in req_data:
			changes = ecMgr.doExtractChanges(req_data['changesUrl'])
			if changes:
				if "edits" in changes:
					for e in changes['edits']:
						print(e)
						# DO SOMETHING HERE 
						# With the results you could save to file, email, automate, etc
				else:
					print("No edits found in response")
						
		else:
			print("No changesUrl found in payload: might not be a correct webhook message")

		return '{"success":"true"}'

if __name__ == "__main__":   
	# Certificate and key file. Cannot be self signed certs
	context = ('ssl.cert', 'ssl.key')
	# Listen on port 5000
	app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True) 
