import boto3
import json
import uuid
import time

region = 'ap-northeast-1'
s3 = boto3.client('s3', region)

bucket = str(uuid.uuid1())
print('bucket:', bucket)
s3.create_bucket(
    Bucket=bucket,
    CreateBucketConfiguration={'LocationConstraint': region})
policy_json = {
    "Version": "2012-10-17",
    "Id": "ForecastS3BucketAccessPolicy",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "forecast.amazonaws.com"
            },
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::"+bucket,
                "arn:aws:s3:::"+bucket+"/*"
            ]
        }
    ]
}
s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy_json))
file_name = 'temperature.csv'
s3.upload_file(file_name, bucket, file_name)

iam = boto3.client('iam')
role_arn = iam.get_role(RoleName='ForecastRole')['Role']['Arn']

forecast = boto3.client('forecast', region)
for dataset in forecast.list_datasets()['Datasets']:
    if dataset['DatasetName'] == 'MyDataset':
        break
dataset_arn = dataset['DatasetArn']

job_arn = forecast.create_dataset_import_job(
    DatasetImportJobName='MyJob',
    DatasetArn=dataset_arn,
    DataSource={'S3Config': {
        'Path': 's3://'+bucket+'/'+file_name, 'RoleArn': role_arn}},
    TimestampFormat='yyyy-MM-dd hh:mm:ss')['DatasetImportJobArn']
print('job ARN:', job_arn)

start = time.time()
status = ''
while status in ['CREATE_PENDING', 'CREATE_IN_PROGRESS']:
    status = forecast.describe_dataset_import_job(
        DatasetImportJobArn=job_arn)['DatasetImportJob']['Status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))
