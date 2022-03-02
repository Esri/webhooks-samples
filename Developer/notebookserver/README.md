# [Notebook Server](https://enterprise.arcgis.com/en/notebook/)

Starting with ArcGIS Enterprise 10.9, ArcGIS Notebook Server can be configured as a webhook receiver for Portal webhooks. The webhook call will execute the code within a given notebook. Using Notebook Server is a great alternative  to setting up an independent server as you can leverage many different Python modules, including the [ArcGIS API for Python](https://developers.arcgis.com/python/).

### Setup

Prior to setting up the webhook, you must have an existing notebook (itemID). Create your Portal webhook by *omitting* the payload URL and using the following JSON for the **config** parameter with your ItemID.

`{
  "deactivationPolicy": {
    "numberOfFailures": 5,
    "daysInPast": 5
  },
  "properties": {
    "federatedServer": {
      "itemId": "<Notebook item id to be executed>",
      "tokenTypeToSend": "owner",
      "tokenExpirationTimeMinutes": 10
    }
  }
}
`
 Consult the [documentation](https://enterprise.arcgis.com/en/notebook/latest/administer/windows/automate-notebook-execution.htm) for detailed steps.

 **Note**: Notebook Server is only available for ArcGIS Portal webhooks. It cannot be the receiver for ArcGIS Online Hosted Features.
