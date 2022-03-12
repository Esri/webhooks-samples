# Creating a feature service webhook receiver with TypeScript and node.js

A sample node app that can receive and process [hosted feature service webhooks](https://developers.arcgis.com/rest/services-reference/online/web-hooks-feature-service-.htm). This example shows the complete workflow to receive the payload and make additional authenticated requests to get the actual features that were edited. The edits are printed to the console.

## Getting Started

1. Ensure you have installed [Node.js](https://nodejs.org)
2. Install dependencies with `npm install`
3. Create and configure a `.env` file with these properties:
```
PORT=3000
SIGNATURE_KEY=<your key>
USERNAME=<your username>
PASSWORD=<your password>
PORTAL=https://arcgis.com/sharing/rest
```
3. Run it locally `npm run serve`

## Deploying

A `Dockerfile` and `docker-compose.yml` file are provided to make it easy to deploy on a server.

1. Run `docker-compose up --build` to build an image and launch a container that runs the receiver.

## Using it

1. In ArcGIS Online you can [create a hosted feature service webhook](https://developers.arcgis.com/rest/services-reference/online/web-hooks-create-feature-service-.htm) and provide the URL and signature key to your webhook receiver (e.g. `https://<hostname>.<domain>.<tld>/webhooks/receive`)

2. Deploy the receiver on a publicly accessible server that can has the specified port opened.

3. Add or edit a feature. You should see the edits printed to the console.