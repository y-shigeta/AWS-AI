import boto3

forecast = boto3.client('forecast')

for group in forecast.list_dataset_groups()['DatasetGroups']:
    group_arn = group['DatasetGroupArn']
    print('dataset group ARN:', group_arn)
    forecast.delete_dataset_group(DatasetGroupArn=group_arn)

for dataset in forecast.list_datasets()['Datasets']:
    dataset_arn = dataset['DatasetArn']
    print('dataset ARN:', dataset_arn)
    forecast.delete_dataset(DatasetArn=dataset_arn)
