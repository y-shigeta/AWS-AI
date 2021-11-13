import boto3
import json

forecast = boto3.client('forecast')

schema_json = {
    "Attributes": [
        {
             "AttributeName": "timestamp",
             "AttributeType": "timestamp"
        },
        {
             "AttributeName": "target_value",
             "AttributeType": "float"
        },
        {
             "AttributeName": "item_id",
             "AttributeType": "string"
        }
    ]
}
dataset_arn = forecast.create_dataset(
    Domain='CUSTOM', DatasetType='TARGET_TIME_SERIES',
    DatasetName='MyDataset', DataFrequency='M',
    Schema=schema_json)['DatasetArn']
print('dataset ARN:', dataset_arn)

group_arn = forecast.create_dataset_group(
    DatasetGroupName='MyGroup', Domain='CUSTOM',
    DatasetArns=[dataset_arn])['DatasetGroupArn']
print('dataset group ARN:', group_arn)
