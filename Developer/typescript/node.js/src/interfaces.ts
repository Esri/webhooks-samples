import { ChangeType, JobStatus } from "./enums";

export interface WebhookPayload {
  layerId?: number,
  serviceName: string,
  changeType: ChangeType,
  orgId?: string,
  changesUrl: string
}

export interface ExtractChangesResponse {
  statusUrl: string
}

export interface StatusResponse {
  status: JobStatus
  resultUrl?: string
}

export interface LayerServerGen {
  id: number
  serverGen: number
}

export interface LayerEdits {
  id: number
  features: Array<FeatureEdits>
}

export interface Feature {
  geometry?: object
  attributes: object
}

export interface FeatureEdits {
  adds: Array<Feature>
  updates: Array<Feature>
  deleteIds: Array<string>
}

export interface ExtractChangesResult {
  layerServerGens: Array<LayerServerGen>
  transportType?: 'esriTransportTypeUrl'
  responseType: 'esriDataChangesResponseTypeEdits'
  edits: Array<LayerEdits>
}
