## This script listens to the 

# Import libraries
import os

print("Running")


#!/usr/bin/python
import time
import admin_assistant
#import debugScript
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
            #debugScript.slackBot()
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
