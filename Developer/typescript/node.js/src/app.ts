import 'dotenv/config'
import express, { Request, Response } from 'express'
import { WebhookPayload, ExtractChangesResponse, StatusResponse } from './interfaces'
import { JobStatus } from './enums'
import { UserSession } from '@esri/arcgis-rest-auth'
import { setDefaultRequestOptions, request } from '@esri/arcgis-rest-request'
import { BinaryLike, createHmac, timingSafeEqual } from 'crypto'

// Required for @esri/arcgis-rest-request with node
// https://esri.github.io/arcgis-rest-js/guides/
const fetch = require('node-fetch')
require('isomorphic-form-data')

// @ts-ignore
setDefaultRequestOptions({ fetch })

declare module 'http' {
  interface IncomingMessage {
    rawBody: unknown;
  }
}

const app = express()
const port = process.env.PORT
const username = process.env.USERNAME
const password = process.env.PASSWORD
const portal = process.env.PORTAL

const userSession = new UserSession({
  username: username,
  password: password,
  portal: portal
})

// Enable some middleware to expose the raw body of a request
app.use(express.json({
  verify: (req, _res, buf) => {
    req.rawBody = buf.toString('utf8')
  }
}))

/**
 * Handles an incoming webhook request
 */
const handleWebhook = (request: Request, response: Response) => {
  if (request.method === 'GET') {
    handleCRC(request, response)
  } else if (request.method === 'POST') {
    if (isValidSender(request)) {
      response.on('finish', () => processPayload(request.body as Array<WebhookPayload>, userSession))
    }
    response.status(200).json()
  }
}

/**
 * Checks that the request is coming from a verified sender by computing the HMAC-SHA256 of the body 
 * and comparing it with the signature sent in the header
 */
const isValidSender = (request: Request): boolean => {
  const hmac = createHmac('sha256', process.env.SIGNATURE_KEY).update(request.rawBody as BinaryLike).digest('base64')
  try {
    const signature = decodeURIComponent(request.header('x-esrihook-signature')).split('sha256=')[1]
    return timingSafeEqual(Buffer.from(hmac), Buffer.from(signature))
  } catch {
    return false
  }
}

/**
 * Handle a Challenge-Response Checks from the sender
 * Computes the HMAC-SHA256 of the crc_token using the signature key and sends that back to the server
 * If the sent response_token is accepted by the server, the webhook is activated (or remains active)
 */
const handleCRC = (request, response: express.Response<unknown, Record<string, unknown>>) => {
  if (request.query.crc_token) {
    const sha256 = createHmac('sha256', process.env.SIGNATURE_KEY).update(request.query.crc_token as string).digest('base64')
    console.log('CRC check completed, webhook active')
    response.status(200).json({ response_token: `sha256=${sha256}` })
  } else {
    response.status(400).json({ error: 'Unable to create sha' })
  }
}

/**
 * Processes the payload received from the webhook
 */
const processPayload = async (payloads: Array<WebhookPayload>, userSession: UserSession) => {
  try {
    const edits = await extractChanges(payloads[0], userSession)
    console.log('Changes:')
    console.log(JSON.stringify(edits, null, 2))
  } catch (e) {
    console.log(e)
  }
}

/**
 * Extracts the changes from the server using the url sent as part of the payload
 */
const extractChanges = async (payload: WebhookPayload, userSession: UserSession) => {
  const extractChangesResponse = await request(decodeURIComponent(payload.changesUrl), {
    authentication: userSession
  }) as ExtractChangesResponse

  if (!extractChangesResponse.statusUrl) { throw new Error("Failed to get changes") }

  let statusRes = await checkJobStatus(extractChangesResponse.statusUrl, userSession)
  while (statusRes.status !== JobStatus.Completed) {
    if (statusRes.status === JobStatus.Failed) { throw new Error("Failed to extract changes")}
    await sleep(5000)
    statusRes = await checkJobStatus(extractChangesResponse.statusUrl, userSession)
  }
  return await request(statusRes.resultUrl, { authentication: userSession })
}

/**
 * Check the status of an async job
 */
 const checkJobStatus = async (url: string, userSession: UserSession): Promise<StatusResponse> => {
  return await request(url, {
    authentication: userSession,
    params: { f: 'json' }
  }) as StatusResponse
 }

/**
 * A helper method to wait for a period of time
 */
const sleep = (ms: number) => {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

// Register a route to send webhooks to
app.all('/webhooks/receive', handleWebhook)

// start the app on a port
app.listen(port, () => {
  console.log(`Webhook receiver running on ${port}.`)
})
