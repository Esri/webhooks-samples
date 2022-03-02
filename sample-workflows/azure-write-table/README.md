# AzureWebHookReceiver

This workflow builds on the [Azure developer sample](../../Developer/azure/). This version has been enhanced to write payloads to an Azure Table. In addition to writing output to the Azure Table, logging statements are used to stream to the log pipeline, allowing you to monitor and understand the flow of the Function from an incoming payload.

[Microsoft Azure Storage Explorer](https://azure.microsoft.com/en-ca/features/storage-explorer/) offers a quick way to inspect the payloads which have been written to the Azure Table.

## Setup and Deploy

## Deploying your own

#### Setup
Before attempting to deploy the Azure function, you'll need to setup your environment. This sample makes use of Python and VS Code to create an Azure Function. Follow the [Getting started with Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-get-started?pivots=programming-language-python) guide and the [Quickstart: Create a function in Azure with Python using VS Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python) before continuing with the steps below. A subscription to Azure is also required. 

1. Install [Python](https://www.python.org/downloads/) (Version 3.7 - 3.9 only)
2. Install [VS Code](https://code.visualstudio.com/Download)
3. Install [Azure Function Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools)
4. VS Code [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (from market place)
    Select the Python interpreter you installed in step 1
5. VS Code [Azure Functions Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) (from market place)

#### Deploy Function

The *azure-wrute-table* should be copied to an independent folder outside this repository as multiple Azure Functions exist. 

1. From VS Code, select **File** > **Open Folder** and select the location of the copied Function. **Trust** the folder to proceed.
2. If you receive a message informing about a failed virtual environment, create a new one and choose your Python interpreter.
3. Select the **Azure** extension (`shift-alt-a`) and **Sign in to Azure** or **Create a free trail**
4. Expand **Local Project** > **Functions** and verify that the **Hook** function exists. The function is an anonymous httpTrigger.
5. Right click the **Hook** function and select **Add binding**
    1. Select **out**
    2. Select **Azure Table Storage**
    3. Provide a **name** (If you choose `outputTable`, you will *not* need to update the code within `__init__py`. Otherwise note the name you provided as it will be required in step 10.)
    4. Provide a **table name** (this will be the table name within the Azure Storage space)
    5. Select **Create new local app setting**
    6. Select an existing or **Create a new storage account**
    7. Provide the **name** for the storage account.
    8. Choose the **resource group** or create a new group.
    9. Select the location for the resource.
    10. (*Optionally* from step 3) Within the `__init__.py` file, update the 4 references to the name you used (Find and replace `outputTable` with your name value)

    `def main(req: func.HttpRequest,  NAME_HERE: func.Out[str]) -> func.HttpResponse:`

    `NAME_HERE.set(json.dumps(data))` (3 instances)

    Wait for the binding to be added to the `function.json`. Once ready, you can test the function locally by pressing **F5**. The receiver will be available at `http://localhost:7071/api/Hook`. A GET request to the URL made within a web browser should return `{"success": true}`


6. Click the Function deploy button on the Azure extension (cloud with up arrow) and select **Create a new function app in azure advanced**
7. Provide a unique name. The name will be used within the URL of your receiver.

    eg. `https://NAME.azurewebsites.net/api/hook`

8. Select a runtime. (Match the version of Python installed)
9. Select the same resource group from the previous Table storage steps
10. Select a location (eg. US East)
11. Select the **consumption** plan
12. Select the same storage account you created in step 5
13. Create an application insight (*optional* this could be useful if you need to debug or stream logs on portal.azure.com)
14. The function will be uploaded to Azure (it could take a few minutes to deploy)
