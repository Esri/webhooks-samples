# Developer Samples
These samples, presented by programming language, provide a quick start for developing a custom receiver that will listen for webhook calls. The code generally takes the payload and writes to a text file. You'll need to enhance the server to suit your business requirements. If you deploy these receivers within your network, behind your firewall, and they cannot be accessed from the general internet, you *cannot* use these as a receiver to ArcGIS Online Hosted Feature Services. ArcGIS.com needs to be able to talk to the receiver. You would need to expose these servers to the internet using a proxy or machine outside your local network. Creating a publicly accessible server is beyond the scope of this help; please work with your IT group or consider a cloud solution.

**Note**: ArcGIS Portal webhooks require a secure receiver, running under HTTP**S**. ArcGIS Online Hosted Feature services can be configured to use a non-secure server. However, you should strongly consider implementing HTTPS. The sample servers listed below may require additional configuration from your IT department before they can run securely.

### [Azure Function](/Developer/azure/function.python)
Azure Functions run serverless code in the cloud. This sample is written in Python, however, an Azure Function can be written in many different languages (C#, JavaScript, F#, Java, PowerShell, TypeScript). This sample logs incoming requests to the Function log stream (payloads are not persisted anywhere).

### [Java](/Developer/java)
This sample requires both a [JDK](https://www.oracle.com/java/technologies/downloads/) (Java Developer Kit) and [Maven](https://maven.apache.org/download.cgi). The sample writes incoming payloads to a text file.

### [JavaScript](/Developer/javascript/node.js)
There are many JavaScript servers. This example uses [Node.js](https://nodejs.org/en/) and makes use of *https*, *fs* and *node-fqdn* modules to listen and write incoming payloads to a text file.

### [TypeScript](/Developer/typescript/node.js)
This example uses [Node.js](https://nodejs.org/en/) and makes use of the *express* framework to receive a hosted feature service webhook payload and make additional authenticated requests to fetch the features that were edited. The results are printed to the console. 

### [Python](/Developer/python/flask)
The Python module, Flask runs a webserver that can listen for GET and POST calls. This example writes the incoming payload to a text file.

### [Notebook Server](/Developer/notebookserver)
ArcGIS Notebook Server can be used as a receiver to Portal webhooks.

## Single Session Testing
These resources can be used for testing and to verify the payload from a webhook which will help you build your solution with a 3rd party website or your custom receiver. These examples are not designed to be used as a complete solution. You generally need to keep the webpage open and manually monitor the payload being received.

### Websites
* [Request Bin](https://requestbin.com/r)
* [Pipe Dream](https://pipedream.com/apps/http/integrations/http) (Can be found from RequestBin, must authenticate)
* [Webhook.site](https://webhook.site/)
* [Request Catcher](https://requestcatcher.com/)

### Software
* [Postman](https://www.postman.com/) (Through a [mock server](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/))

