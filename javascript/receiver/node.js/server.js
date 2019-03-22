/*Copyright 2019 Esri
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.*/

const https = require('https');
const fs = require('fs');

var fqdn = require('node-fqdn');
var port = 8000;

const options = {
  pfx: fs.readFileSync('certificate.pfx'), //PKCS#12 certificate
  passphrase: 'passphrase'
};

https.createServer(options, (req, res) => {

	var d = new Date();
	var n = d.toLocaleTimeString();
	var requestHost = req.headers.host;
	
	  var body = "";
  req.on('data', function (chunk) {
    body += chunk;
  });
  
  req.on('end', function () {  
  try{			
		console.log("-----------------------------"+n+"--------------------------------------------------------------------------------");				
		var s = JSON.parse(body.trim());
		console.log(s);		
		res.end('{"success":"true"}');		
		//write to a file
		  fs.open('C:\\temp\\webhookPayloads.txt', 'a', 666, function( e, id ) {
			fs.write( id, message.text+'\n', null, 'utf8', function(){
    fs.close(id, function(){
      console.log('file closed');
    });
  });
});

	}
	catch(err){
		console.log( n + " Not a JSON " + err.message);		
		res.end('{"success":"false"}');		
		
	}
  
  
  })	
  res.writeHead(200);  
}).listen(port);

var d = new Date();
var n = d.toLocaleTimeString();
console.log(n +' Server running at https://' + fqdn() + ':'+ port  );
