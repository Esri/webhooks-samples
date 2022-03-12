export enum ChangeType {
  FeaturesCreated = 'FeaturesCreated',
  FeaturesUpdated = 'FeaturesUpdated',
  FeaturesDeleted = 'FeaturesDeleted',
  FeaturesEdited = 'FeaturesEdited',
  AttachmentsCreated = 'AttachmentsCreated',
  AttachmentsUpdated = 'AttachmentsUpdated',
  AttachmentsDeleted = 'AttachmentsDeleted',
  LayerSchemaChanged = 'LayerSchemaChanged',
  LayerDefinitionChanged = 'LayerDefinitionChanged',
  FeatureServiceDefinitionChanged = 'FeatureServiceDefinitionChanged'
}

export enum JobStatus {
  Completed = 'Completed',
  Pending = 'Pending',
  Failed = 'Failed'
}
