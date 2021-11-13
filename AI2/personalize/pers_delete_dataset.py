import boto3
import time

personalize = boto3.client('personalize')

for dataset in personalize.list_datasets()['datasets']:
    dataset_arn = dataset['datasetArn']
    print('dataset ARN:', dataset_arn)
    personalize.delete_dataset(datasetArn=dataset_arn)

for group in personalize.list_dataset_groups()['datasetGroups']:
    group_arn = group['datasetGroupArn']
    print('dataset group ARN:', group_arn)
    while True:
        try:
            personalize.delete_dataset_group(
                datasetGroupArn=group_arn)
        except Exception:
            time.sleep(1)
            break

for schema in personalize.list_schemas()['schemas']:
    schema_arn = schema['schemaArn']
    print('schema ARN:', group_arn)
    while True:
        try:
            personalize.delete_schema(schemaArn=schema_arn)
        except Exception:
            time.sleep(1)
            break
