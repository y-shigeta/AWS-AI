import boto3
import json
import time

personalize = boto3.client('personalize')

schema_json = {
    "type": "record",
    "name": "Interactions",
    "namespace": "com.amazonaws.personalize.schema",
    "fields": [
        {
            "name": "USER_ID",
            "type": "string"
        },
        {
            "name": "ITEM_ID",
            "type": "string"
        },
        {
            "name": "TIMESTAMP",
            "type": "long"
        }
    ],
    "version": "1.0"
}
schema_arn = personalize.create_schema(
    name='MySchema', schema=json.dumps(schema_json))['schemaArn']
print('schema ARN:', schema_arn)

group_arn = personalize.create_dataset_group(
    name='MyGroup')['datasetGroupArn']
print('dataset group ARN:', group_arn)

start = time.time()
status = ''
while status not in ['ACTIVE', 'CREATE FAILED']:
    status = personalize.describe_dataset_group(
        datasetGroupArn=group_arn)['datasetGroup']['status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))

dataset_arn = personalize.create_dataset(
    name='MyDataset', datasetType='interactions',
    schemaArn=schema_arn, datasetGroupArn=group_arn)['datasetArn']
print('dataset ARN:', dataset_arn)
