'''
Copyright 2019 Esri
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

################################################################################
##            	  Slack Assistant             
#                 Nalika & Joel  - 05/29/2019
#
#   This script reads a textfile that is being written to by
#   a Java servlet, after it has recieved payloads from Portal. It goes through
#   the event and looks for events where an item has been shared to
#   the public.  If it finds an item, then it calls back into Portal
#   to check if the item has the appropriate tags, description, completeness score
#   to be shared to Portal.  If it does not, a Slack message is sent to the admins
#   and they are asked if they want to unshare the item
#
##
################################################################################

#Set the parameters in the config.py file to run this script
from config import *  

def slackBot():

# Import libraries
    import os         
    import json
    from arcgis.gis import GIS            # with anaconda installed, conda install -c esri arcgis
    from slackclient import SlackClient   # pip install slackclient 
    slack = SlackClient(slackToken)
    
    # Set path to folder where webhookPayloads.txt file is being written to (based on java application)
    os.chdir('c:\\temp')

    # Open textfile in read mode
    textFile = open("webhookPayloads.txt","r+")
	
    # Run if the textfile has something 
    if os.stat("c:\\temp\\webhookPayloads.txt").st_size>0:

        # String formatting
        width = os.get_terminal_size().columns
        stars = ("*"*width)
        dash = ("_"*width)

        # Title of the script
        print(stars)
        print("Portal Admin assistant".center(width))
        print("I will let you know if items shared to the public meet our organization standards.".center(width))
        print(stars)


        ###########################################
        ##  Step One:
        ##   -Convert textfile lines to JSON items
        ##   -Then parse through data
        ##   -Determine what type of operation
        ##   triggered the webhook
        ###########################################

        # Set path to grab webhookPayloads.txt file
        os.chdir('c:\\temp')

        # Open textfile in read mode
        textFile = open("webhookPayloads.txt","r+")
        events = textFile.readlines()

        # Initialize JSON list for each event
        jsonEvents=[]

        # Loop through the events
        for event in events:

            # Convert event in textfile to JSON, and append to JSON list
            try:
                jsonEvents.append(json.loads(event))

            # If the string cannot be converted to JSON show this exception
            except:
                print("\nCould not convert to JSON")


        ###########################################
        ##   Parse through data
        ###########################################        

        print("...")
		

        # Keep count of payloads being processed 
        payloadCount = 0
        shareEvents = 0
        publiclyShared = 0
        portalURL = jsonEvents[0]['info']['portalURL']
        print("It looks like there are %s payloads that were received from \n%s which have not been processed yet" %(str(len(events)),portalURL))

        # Connect to GIS portal
        print("...")
        gis = GIS(portalURL, portalUsername, portalPassword)
        print("Parsing through events...")

        descriptionText = ""
        itemScoreText = ""
        tagsText = ""


        # Loop through each event to examine the payload
        for event in jsonEvents:
            
            # Find out what kind of operation it was
            operation = event['events'][0]['operation']
            user = event['events'][0]['username']


            # Was the operation a share event?
            if operation =="share":
                # If so, who was it shared to?
                sharedTo = event['events'][0]['properties'].get("sharedToGroups")

                ###########################################
                ##  Step Two:
                ##   -If the item was shared to everyone,
                ##   then check the item's properties. 
                ###########################################
                
                # While that item is shared to everyone, then process this event
                if sharedTo[0] == "Everyone":
                    # Score to decide if the item should be shared to the public
                    score = 1

                    # Required tags to use as reference
                    requiredTags = standardTags

                    #Get item ID from the payload and use it to call into Portal
                    itemID = event['events'][0]['id']
                    sharedItem = gis.content.get(itemid=itemID)

                    print(dash)
                    print("The following item was shared publicly: %s" %(sharedItem))
                    print(sharedItem.homepage)
                    print("\nChecking for item completeness... ")
                    print("...\n")
                    print("-----------------------")
                    print("Check #1: Required Tags")
                    print("-----------------------")
                    # For each tag in the item's current tags
                    for tag in sharedItem.tags:

                        # If the current tag is in the list of required tags
                        if tag in requiredTags:

                            #Remove that tag
                            requiredTags.remove(tag)

                    # Once we have compared the tags in the item to the required tags, lets see what tags remain.  
                    if (len(requiredTags) == 0):
                        print("Item has all the required tags.")
                        tagsText = "Item has all the required tags."
                    elif (len(requiredTags) >=1):                 
                        print("The item is missing the following tags: ", requiredTags)
                        score = (score-1)
                        tagsText = "The item is missing the following tags: %s" %(requiredTags)

                    print("\n-----------------------")
                    print("Check #2: Description")
                    print("-----------------------")

                    try:

                        if len(sharedItem.description)<30:
                            print("Item description is not long enough.")
                           # score = (score-1)
                            descriptionText = "Item description is not long enough."
                    except:
                        print("No item description was entered.")
                        #score = (score-1)
                        descriptionText = "No item description was entered."

                    print("\n-----------------------------")
                    print("Check #3: Completeness Score")
                    print("-----------------------------")

                    if sharedItem.scoreCompleteness < 70:
                        print("Score completeness is currently", sharedItem.scoreCompleteness,"%. \nTo share this item publicly the min. completeness score must be 70%")
                       # score = (score-1)
                        itemScoreText = "Score completeness is not at least 70%"

                    print("\n-----------------------------")
                    print("FINAL VERDICT")
                    print("-----------------------------")

                    # Check the final score of the item, to determine whether the item was ready to be shared publicly or not. 
                    if score<1:
                        print("This item is not ready to be shared to the public.  See results above.\n")

                        ###########################################
                        ##  Step Three:
                        ##   - Alert the Slack channel, using Slack's
                        ##    API
                        ##   - This is how the initial message from
                        ##     the bot is constructed. 
                        ###########################################

                        slack.api_call(
                        "chat.postMessage",
                        channel="managers",
                        text="*The following item was shared to the collaboration group, but does not meet all of the requirements:*",
                            attachments= [
                            {
                                "fallback": "Required plain-text summary of the attachment.",
                                "title": "%s"%(sharedItem),
                                "title_link": "%s"%(sharedItem.homepage),
                                "text": "Item was shared by: *%s*" %(user),
                                "fallback": "You are unable to choose an option",
                                "fields": [
                                {
                                "title": "Tags",
                                "value": "%s" %(tagsText)
                                },
                                {
                                "title": "Description",
                                "value": "%s" %(descriptionText)
                                }, 
                                    {
                                "title": "Score completeness",
                                "value": "%s" %(itemScoreText)
                                    },
                                     {
            "title": "How would you like to proceed?",
            "value": "To update the tags enter the following command: add tags: your,tags,here"
                }],
                                "callback_id": "option",
                                "color": "#3AA3E3",
                                "attachment_type": "default"
                                }],
                        reply_broadcast=True
                         )

                    else:
                        print("Item was successfully shared to the public, and meets all requirements\n")

        textFile.truncate(0)

    else:
        print("Text file empty")


# This function is called only when a response is received in Slack.  The response will be
# written to a textfile, which will include the actions the user would like to take.
# Alternatively, you can edit the function above to automatically update the tags without requiring a
# response from the user in slack.

def responseHandler():

    # Import libraries
    import os
    import json
    from arcgis.gis import GIS            # with anaconda installed, conda install -c esri arcgis
    from slackclient import SlackClient   # pip install slackclient 
    slack = SlackClient(slackToken)

    gis = GIS(portalFQDN, portalUsername, portalPassword)
    
    os.chdir('c:\\temp')
    # Open textfile in read mode
    slackFile = open("response.txt","r", encoding='utf-8-sig')

    # Each event is separated by a \n in the textfile

    #Sample command: "Unshare item"
    unshareCommand = "unshare item "
    unshare = False

    addTagCommand = "add tags:"
    addTag = False

    response = slackFile.readlines()
    response = response[0]
    response = response.rstrip('\n')
    
    #Is it the unshare command
    testResponse1 = response[:12]

    tags=[]

    #Is it the add tag command
    testResponse2 = response[:9]


    if testResponse1.lower()==unshareCommand:
            try: 
                    itemCommand = response[13:]
                    response = response.rstrip(itemCommand)
            except:
                    print("No Item ID or invalid command")

    elif testResponse2.lower() == addTagCommand:
                try: 
                    getTags = response[10:]
                    getTags = getTags.split(", ")


                    for tag in getTags:
                        tags.append(tag)

                    print(tags)
                    strippedTags = ' '.join(tags)
                    print(strippedTags)
                    #print(strippedTags)
                    strippedTags = strippedTags.replace(" ",",")
                    print(strippedTags)

                    portalItem = gis.content.get(itemid=searchItemID)
                    #portalItem.update(item_properties={'tags':'python, vei, empirical, in-situ'})
                    print(strippedTags)
                    portalItem.update(item_properties={'tags':'%s'%strippedTags})

                except:
                    print("No tags were entered")

    else:
            print("Not a valid command")
