# [Power Automate](https://powerautomate.microsoft.com/en-us/)

Power Automate (previously Microsoft Flow) provides a webhook connector to build workflows.

### Quick Start

Create a new flow.

1. Click **+ Create** 
2. Choose **Automated cloud flow**
3. Click **Skip**
4. From the search, enter `"http"`.
5. From **Triggers** section, choose **When an HTTP request is received**
6. Copy the [sample payload from below](#sample-payloads) for Portal or Feature Service webhooks and paste it into the **Request Body JSON Schema**.
7. Click the **+** button and choose and configure the next action(s) to complete your flow.
8. Click **Save**.
9. Copy the URL by clicking the paper icon beside the URL in the **When an HTTP request is received** connector. Use the URL to setup the webhook within ArcGIS Portal or ArcGIS Online Hosted Feature Services

### Quick Start - ArcGIS Online Hosted Feature Service

The previous instructions are valid for both Hosted Feature Services and Portal webhooks. 

A [Survey123](https://docs.microsoft.com/en-us/connectors/survey123/#when-a-survey-response-is-submitted) specific connector is available to quickly use in place of the **When an HTTP request is received** connector. When using this connectors, it will authenticate with ArcGIS Online and allow you to select the Hosted Feature Service you want to use in your workflow. The connector will automatically create the webhook on the service, allowing you to skip this ArcGIS.com configuration step.
  
[Setup a Survey123 webhook in Power Automate](https://doc.arcgis.com/en/survey123/browser/create-surveys/webhooks.htm#ESRI_SECTION1_C52B77E37FAD462AB58F09982E381240)

### Security and Secret Keys

Both ArcGIS Online Feature Service and Portal webhooks have the ability to send a webhook payload with a known secret key. The receiver must be able to extract the secret key from the payload, compare the value to it's known key and decide if the incoming payload is trusted and proceed accordingly. 

Portal webhooks make use of the `secret` parameter when setting up the hook. This value will be passed through HTTPS and can be read by the reciever within the incoming request's header. A simple comparison of the known secret key to the incoming secret value can be used to determine if the message can be trusted.
Make use of the following data operation's within Power Automate:
* Initialize variable (Create a string variable `secretkey` and set the value to the same secret key used in the webhook)
* Parse JSON (Headers content)
* Compose (Get the secret parameter from the header: `body('Parse_JSON')?['secret']`)
* Condition 
  * Check if the incoming secret value (`outputs('Compose')`) is equal to the known secret (`variables('secretkey')`)
  * If yes, perform a trusted action
  * If no, perform a different action (or no action at all)

ArcGIS Online Feature Service webhooks make use of a Challenge-Response Checks to ensure trust. With the trust established, all payloads send a SHA256 hash in the header of the response using the `x-esriHook-Signature`. With trust established, the receiver must make use it's known secret key and generate a hash from the payload. If this hash matches the signature from the incoming payload, the message can be considered trusted.

#### Sample Payloads

**ArcGIS Portal webhooks schema**
```json
{
    "type": "object",
    "properties": {
        "info": {
            "type": "object",
            "properties": {
                "webhookId": {
                    "type": "string"
                },
                "webhookName": {
                    "type": "string"
                },
                "portalURL": {
                    "type": "string"
                },
                "when": {
                    "type": "integer"
                }
            }
        },
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "userId": {
                        "type": "string"
                    },
                    "username": {
                        "type": "string"
                    },
                    "when": {
                        "type": "integer"
                    },
                    "operation": {
                        "type": "string"
                    },
                    "source": {
                        "type": "string"
                    },
                    "id": {
                        "type": "string"
                    },
                    "properties": {
                        "type": "object",
                        "properties": {}
                    }
                },
                "required": [
                    "userId",
                    "username",
                    "when",
                    "operation",
                    "source",
                    "id",
                    "properties"
                ]
            }
        }
    }
}
```

**ArcGIS Online Feature Service webhooks schema**
```json
{
    "type": "object",
    "properties": {
        "layerId": {
            "type": "integer"
        },
        "serviceName": {
            "type": "string"
        },
        "changeType": {
            "type": "string"
        },
        "orgId": {
            "type": "string"
        },
        "changesUrl": {
            "type": "string"
        }
    }
}
```
