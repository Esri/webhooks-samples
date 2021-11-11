/*Copyright 2021 Esri
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
   
   // Portal requires the receiver to be running HTTPS
   // Different options exist to enable HTTPS for your NodeJS server
   // Once configured, use the checkUrl of your Portal to ensure your certs and trust chain
   // are configured correctly:  https://yourPortal/portal/sharing/rest/portals/checkUrl
   var key = fs.readFileSync('theKey.key');
   var cert = fs.readFileSync('theCert.crt');
   const options = {
       key: key,
     cert: cert
   };
   
   https.createServer(options, (req, res) => {
     
     if (req.method == "GET"){
       res.writeHead(200, { "Content-Type": "text/html" });
       res.end('Thank you for the GET, try a POST')
     }
     else { //assume POST  
   
       var d = new Date();
       var n = d.toLocaleTimeString();
       //console.log("headers: ", req.headers)
       
       var body = "";
       req.on('data', function (chunk) {
         body += chunk;
       });
       
       req.on('end', function () {  
       try{			
         console.log("-----------------------------"+n+"------------------------------------");	
         if (body){
           var s = JSON.parse(body.trim());
           console.log(s);	
           res.end('{"success":"true"}');		
           //write to a file
           fs.open('C:\\temp\\webhookPayloads.txt', 'a', 666, function( e, id ) {
             fs.write( id, JSON.stringify(JSON.parse(body.trim()))+'\n', null, 'utf8', function(){
               fs.close(id, function(){
                 console.log('file closed');
               });
             });
           });
         } else {
           res.end('{"success":"no body found"}');	
         }				
       }
       catch(err){
         console.log( n + " Error handling incoming POST: " + err.message);		
         res.end('{"success":"false"}');			
       }	  
         
       })	
       res.writeHead(200);  
     }
   }).listen(port);
   
   var d = new Date();
   var n = d.toLocaleTimeString();
   console.log(n +' Server running at https://' + fqdn() + ':' + port );
   