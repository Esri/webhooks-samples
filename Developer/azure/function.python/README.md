
# AzureWebHookReceiver

The following samples provides a webhook receiver, designed to run on Azure and handle messages from an ArcGIS Online Feature service (it will also support Portal webhooks). Once deployed to Azure, a secure, public URL allows webhooks to send payloads to the receiver. This sample will only listen for messages and write the output to the logger. Further development is required to complete the workflow. Within the samples, a copy of this has been enhanced to [log payloads into an Azure Table](../../../sample-workflows/azure-write-table/). Alternatively you could write the messages into a Queue or make use of other Python modules to perform actions.

**Note**: The receiver will support the AGOL `secret key` implementation of the SHA256 hash. Update the `SECRETKEY` value in the `hash_check.py` file. This implementation is specific to the ArcGIS Online [secret key workflow](https://developers.arcgis.com/rest/services-reference/online/web-hooks-security-feature-service-.htm). Portal webhooks do not make use of the 256 hash, as such the code would have to be updated to listen and respond to a secret key from Portal. The receiver you deploy as a function will be available to anyone who can find the URL unless you take steps to secure the endpoint. Various mechanisms within Azure Functions and Azure itself exist, however these topics are not covered here.


## Setup and Deploy

#### Setup
Before attempting to deploy the Azure function, you'll need to setup your environment. This sample makes use of Python and VS Code to create an Azure Function. Follow the [Getting started with Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-get-started?pivots=programming-language-python) guide and the [Quickstart: Create a function in Azure with Python using VS Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python) before continuing with the steps below. A subscription to Azure is also required. 

1. Install [Python](https://www.python.org/downloads/) (Version 3.7 - 3.9 only)
2. Install [VS Code](https://code.visualstudio.com/Download)
3. Install [Azure Function Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools)
4. VS Code [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (from market place)
 * Select the Python interpreter you installed in step 1
5. VS Code [Azure Functions Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) (from market place)

#### Deploy Function

The code from the repistory should be copied to an indpendent folder outside this repistory as multiple Azure Functions exist. 

1. From VS Code, select **File** > **Open Folder** and select the location of the copied Function. **Trust** the folder to proceed.
2. If you receive a message informing about a failed virtual environment, create a new one and select your Python interpreter.

You can test the function locally by pressing **F5**. Once ready, the receiver will be available at `http://localhost:7071/api/Hook`

3. Select the **Azure** extension (`shift-alt-a`) and **Sign in to Azure** or **Create a free trail**
4. Expand **Local Project** > **Functions** and verify that the **Hook** function exists. The function is an anonymous httpTrigger.
5. Click the Function deploy button on the Azure extension (cloud with up arrow) and select **Create a new function app in azure advanced**
6. Provide a unique name. The name will be used within the URL of your receiver.

  eg. `https://NAME.azurewebsites.net/api/hook`

7. Select a runtime. (Match the version of Python installed)
8. Create a new or select an existing resource group
9. Select a location (eg. US East)
10. Choose the **consumption** plan
11. Create a new storage account an provide a name
12. Create an application insight (*optional* this could be useful if you need to debug or stream logs on portal.azure.com)
13. The function will be uploaded to Azure (it could take a few minutes to deploy)


### Example
Chase Clark, GIS Analyst at Stantec presented a video, [Integrating webhooks, serverless functions and web tools for real-time updates](https://www.esri.com/videos/watch?videoid=V0XN133K7Sw&title=integrating-webhooks-serverless-functions-and-web-tools-for-real-time-updates) describing the use of an Azure Function to handle webhook responses.
