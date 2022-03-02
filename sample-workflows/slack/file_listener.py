"""  Copyright 2019 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """
    
# Import libraries
import os

print("Listening for changes...")


#!/usr/bin/python
import time
import admin_assistant

#Ensure you've installed the watchdog library 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_modified(payLoadFile, event):
        
        #print(f'event type: {event.event_type}  path : {event.src_path}')
        editedFile = event.src_path
        
        # Either the webhookPayloads.txt will be uploaded if a payload is received, or
        # the response.txt file will be uploaded if a message is sent to our slack bot
        if editedFile == "/temp/webhookPayloads.txt":
            admin_assistant.slackBot()
        elif editedFile =="/temp/response.txt":
            admin_assistant.responseHandler()
        

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/temp/', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
