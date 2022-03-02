# Getting started with Webhooks
A webhook is generally regarded as an application that will send a notification when an event occurs. The key here, is an event and the occurring action differs from web applications that must reach out and make requests to other applications. In the ArcGIS world, webhooks are a powerful mechanism that facilitates automation by allowing discrete tasks to be chained together. Think of an important business problem: I need to know when a new row is created in my table. Or, more clearly defined in the ArcGIS world: Send me an email when someone completes a survey. The alternative would require an individual to go and manually check a feature service or write a script to periodically poll a RESTful service. Webhooks are the piece between the feature service action (new record) and the notification email.
Webhooks were first introduced to Survey123 in 2018, followed closely by Portal webhooks (ArcGIS Enterprise 10.7) in 2019 and most recently, ArcGIS Online Hosted Feature Services introduced support in 2020. We plan on adding more webhook support within ArcGIS Enterprise in the near term.

The best place to start learning about webhooks within ArcGIS products is the official help.
* [Portal](https://enterprise.arcgis.com/en/portal/latest/administer/windows/create-and-manage-webhooks.htm)
* [Portal (REST)](https://developers.arcgis.com/rest/users-groups-and-items/create-webhooks.htm)
* [Survey123](https://doc.arcgis.com/en/survey123/browser/create-surveys/webhooks.htm)
* [ArcGIS Online Hosted Feature Services](https://developers.arcgis.com/rest/services-reference/online/web-hooks-feature-service-.htm)

This repository will focus on the resources required to complete your automation using webhooks. Some consider implementing a webhook to be a "developer" task. Setting up a custom server to listen for webhook calls could  certainly be considered a developer task, however many websites offer low to no-code solutions that listen for webhook messages. If you're familiar with ModelBuilder or Visio, setting up a webhook on these websites will feel familiar. 

# Samples to get you started
Within this repository are starter samples. They have been grouped into [Developer](/Developer) and [3rd Party](/3rdParty). You'll probably choose a commercial vendor or custom solution based on your business requirements. If you are still in the testing or experimentation stage of webhook development, check the [developer readme](/Developer/README.md) for websites that offer quick, session-based receivers that listen for webhook payloads.

- Download the entire repository. From the **Code** button near the top, **Download Zip** or using git tools: `git clone git@github.com:Esri/webhooks-samples.git`


### Custom Receivers
Deploying a custom receiver (HTTP Server) is a good option for responding to webhooks if any of the following are true:
* You have the hardware to run a dedicated server
* You have the technical expertise to develop and maintain a custom server
* You need to keep communications within your network
* Your business needs require a custom solution not offered by an existing vendor

The following receivers are grouped by programming language. The result of each is pretty much the same, a basic server that listens on a given port and writes the incoming payload to a text file. In practice, you will need to enhance the server to fulfill your business need; perhaps [sending an email](/sample-workflows/python-email) after receiving a particular message.
* [Webhook receiver via Node.js](/javascript/node.js)
* [Webhook receiver via Python](/Developer/python/flask) 
* [Webhook receiver via Java](/Developer/java)
* [Webhook receiver via Azure](/Developer/azure/function.python) - Cloud-based receiver written in Python
* [Webhook receiver via ArcGIS Notebook Server](/Developer/notebookserver)

### 3rd Party (Commercial) Receivers
Many websites offer free, low cost or subscription-based services that you can quickly get started. We don't recommend one vendor over another; based on your business requirements you can evaluate each vendor and choose the one who best fits your needs. The following list represents just some of the 3rd party websites you can explore and leverage. For each of the providers below, we describe how to get started and provide samples or templates (if appropriate).
* [IFTTT](/3rdParty/IFTTT)
* [Make (previously Integromat)](/3rdParty/Make) 
* [Microsoft Power Automate (previously Flow)](/3rdParty/PowerAutomate)
* [Tray.IO](/3rdParty/Tray.IO)
* [Zapier](/3rdParty/Zapier)


### Workflow samples
Explore some of the more [complete "end to end" examples](/sample-workflows). These are a mix of 3rd party and custom solutions that might provide a jump start or just give you an idea on how to accomplish your task.
* [Using an AWS Lambda function](https://www.esri.com/arcgis-blog/products/arcgis-enterprise/administration/webhooks-dev-summit-2019/) (Blog + Video)
* [Slack bot notifies new items with incomplete metadata](/sample-workflows/slack)
* [A Python Flask server to send emails](/sample-workflows/python-email)
* [Write payloads from an Azure Function to an Azure Table storage](/sample-workflows/azure-write-table)
 
## Resources

* [Webhooks - Don't call us, we'll call you (Portal - blog)](https://www.esri.com/arcgis-blog/products/arcgis-enterprise/administration/webhooks-dont-call-us-well-call-you/)
* [Using Webhooks in ArcGIS Enterprise (Portal - video)](https://www.esri.com/videos/watch?videoid=aX4VhaonTFg&title=using-webhooks-in-arcgis-enterprise)
* [Create a hosted feature service webhook (blog)](https://www.esri.com/arcgis-blog/products/arcgis-online/sharing-collaboration/how-to-create-a-hosted-feature-service-webhook/)
* [Getting Started with Hosted Feature Layer Webhooks (video)](https://www.esri.com/videos/watch?videoid=D9PMC2yGJbA&title=getting-started-with-hosted-feature-layer-webhooks)
* [Use webhooks to automate workflows in ArcGIS Field Maps with Power Automate (Feature Service - blog)](https://www.esri.com/arcgis-blog/products/field-maps/field-mobility/use-webhooks-to-automate-workflows-in-arcgis-field-maps-with-power-automate/)
* [Create ArcGIS Workflow Manager Jobs Using Survey123 Webhooks (blog)](https://www.esri.com/arcgis-blog/products/workflow-manager/field-mobility/create-arcgis-workflow-manager-jobs-using-survey123-webhooks/)
* [Use webhooks to automate workflows in ArcGIS Field Maps (Feature Service - blog)](https://www.esri.com/arcgis-blog/products/field-maps/field-mobility/use-webhooks-to-automate-workflows-in-arcgis-field-maps/)


## Issues

Find a bug? Does a sample require more information? Do you have another resource to suggest? Please let us know by submitting an [issue](https://github.com/Esri/webhooks-samples/issues).

## License
Copyright 2019 - 2022 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's [license.txt]( /LICENSE) file.
