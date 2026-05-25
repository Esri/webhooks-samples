# [ArcGIS Notebook Server](https://enterprise.arcgis.com/en/notebook/)

## Organization and Service webhooks to Notebook Server

Both organization and service webhooks can be directed to ArcGIS Notebook Server. The incoming webhook message will ultimately trigger a Python notebook, in turn, running Python code. This pattern enjoys the benefits of leveraging the Notebook Server infrastructure with the flexibility of developer workflows, supported by the ArcGIS API for Python.

### Notebook Server webhook receiver

The release of ArcGIS Notebook Server 11.5 introduced a webhook receiver. Webhook receivers could be enabled, scoped with specific privileges to run and access specific Python code. These receivers provide a payload URL that can be used with ArcGIS webhooks. Prior to the 11.5 release, [Organization webhooks](https://enterprise.arcgis.com/en/notebook/latest/administer/windows/automate-notebook-workflows-with-webhook-events.htm#ESRI_SECTION1_E61B62B25F394778BCE814AA1298083C) could trigger a Python notebook directly (explanation in the [legacy section below](#legacy-pre-arcgis-enterprise-115)). While this workflow is still applicable, the preferred method, which also supports [feature and geoprocessing service](https://enterprise.arcgis.com/en/notebook/latest/administer/windows/automate-notebook-workflows-with-webhook-events.htm#ESRI_SECTION1_AA2CB1134C294DDD830C28BA007DDB8A) webhooks is to create a webhook receiver and use this webhook URL in the webhook creation.

[Consult the detailed documentation](https://enterprise.arcgis.com/en/notebook/latest/administer/windows/automate-notebook-workflows-with-webhook-events.htm#ESRI_SECTION1_AA2CB1134C294DDD830C28BA007DDB8A) to setup a webhook receiver in Notebook Server. For reference, the main requirements involve:
 - An existing Python Notebook (code which is run when the webhook is triggered)
 - Creating an API key scoped with Notebook privileges and permission to the Notebook item and any item the Python code references
 - Creating the receiver within Notebook Server with an exactly 32 character secret key.
 - Creation of the webhook, pointing the payload URL to the newly created webhook receiver and supplying the matching 32 character secret key

### Python code as a webhook receiver

The Python code will be triggered when the webhook payload is received by the webhook receiver. In most instances, the incoming payload will be a necessary part of the workflow; the code will act upon the information inside the payload. This payload is automatically injected into the Python notebook as a variable, `webhookPayload`. 

> [!NOTE]
> 11.5 - 12.0 requires loading the payload as JSON: `json.loads(webhookPayload)`. 12.1 and onwards the `webhookPayload` is injected into the Notebook as a JSON object.

The sample notebook, [Example_FS_ExtractChanges.ipynb](/Notebook/Example_FS_ExtractChanges.ipynb) demonstrates the use of the `webhookPayload` variable. In addition, the sample makes use of a `samplePayload`, a practice of capturing an example webhook payload and developing code against that. Prior to putting the Notebook code into production, the switch from `samplePayload` to `webhookPayload` is necessary.

The example code shows the process of using the `changesUrl` from a feature service payload to work through the [extract changes](https://developers.arcgis.com/rest/services-reference/enterprise/extract-changes-feature-service/) workflow. These steps get the actual change JSON from the feature service, allowing the code to interact with the actual changes that occurred which cause the webhook to trigger. The high-level workflow can be described as:
 - Making a call to the /extractChanges API of a feature service, supplying **serverGens** and return properties
 - This initial call returns a JobID. The job needs to be polled until it has **completed**
 - From the **results** of the job, use the supplied URL to fetch the `.json` file with the x/y and attributes of the changes.

## Legacy (Pre ArcGIS Enterprise 11.5)

**Only use these steps if your ArcGIS Enterprise is older than 11.5**

Starting with ArcGIS Enterprise 10.9, ArcGIS Notebook Server can be configured as a webhook receiver for Portal webhooks. The webhook call will execute the code within a given notebook. Using Notebook Server is a great alternative to setting up an independent server as you can leverage many different Python modules, including the [ArcGIS API for Python](https://developers.arcgis.com/python/).

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

 Consult the [documentation](https://enterprise.arcgis.com/en/notebook/11.3/administer/windows/automate-notebook-execution.htm#ESRI_SECTION1_E61B62B25F394778BCE814AA1298083C) for detailed steps.

 **Note**: Prior to ArcGIS Enterprise 11.5, Notebook Server is only available for Organization webhooks. It could not be the receiver for neither ArcGIS Enterprise or ArcGIS Online Hosted service based webhooks.


