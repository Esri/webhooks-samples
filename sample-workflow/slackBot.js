/*Copyright 2019 Esri
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

PLEASE NOTE: 
This application was created for demonstration purposes.  
Code is not production ready, and requires further testing and modification.

For more information on creating a slack chat bot using Slack and Node see: 
https://github.com/slackapi/node-slack-sdk
https://botkit.ai/docs/v0/readme-slack.html
https://api.slack.com/tutorials/easy-peasy-bots

About this application:
The following application creates a websocket using node.js and 
listens for messages directed at the slack application/bot.  After a message
has been sent to the application, it is written to a textfile so that it can be 
processed by the admin_assistant.py script
*/

//Ensure you have Botkit packages installed
var Botkit = require('botkit')
const fs = require('fs');

var controller = Botkit.slackbot({debug: false})
controller
  .spawn({
	token: 'Your Slack Bot User Oauth Access token'	//edit this line! 
  })
  .startRTM(function (err) {
    if (err) {
      throw new Error(err)
    }
  })

// Log specific message(s) received
controller.hears(

/* This bot was created only for the purpose of adding tags to a portal item
You can edit this function to configure what types of messages to listen for
and how the bot will respond. */
  [" "], ['direct_message', 'direct_mention', 'mention'],
  function (bot, message) { bot.reply(message, 'Adding tags'),
  console.log(message)
  
  //The message sent by a user to the bot will be written to this textfile
  fs.open('C:\\temp\\response.txt', 'a', 666, function( e, id ) {
  fs.write( id, message.text+'\n', null, 'utf8', function(){
    fs.close(id, function(){
      console.log('file closed');
    });
  });
});

})