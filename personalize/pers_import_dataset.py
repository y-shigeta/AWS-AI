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
    "Id": "PersonalizeS3BucketAccessPolicy",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "personalize.amazonaws.com"
            },
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::"+bucket,
                "arn:aws:s3:::"+bucket+"/*"
            ]
        }
    ]
}
s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy_json))
file_name = 'interaction.csv'
s3.upload_file(file_name, bucket, file_name)

iam = boto3.client('iam')
role_arn = iam.get_role(RoleName='PersonalizeRole')['Role']['Arn']

personalize = boto3.client('personalize')

for group in personalize.list_dataset_groups()['datasetGroups']:
    if group['name'] == 'MyGroup':
        break
group_arn = group['datasetGroupArn']

for dataset in personalize.list_datasets(
        datasetGroupArn=group_arn)['datasets']:
    if dataset['name'] == 'MyDataset':
        break
dataset_arn = dataset['datasetArn']

job_arn = personalize.create_dataset_import_job(
    jobName='MyJob', datasetArn=dataset_arn,
    dataSource={'dataLocation': 's3://'+bucket+'/'+file_name},
    roleArn=role_arn)['datasetImportJobArn']
print('job ARN:', job_arn)

start = time.time()
status = ''
while status not in ['ACTIVE', 'CREATE FAILED']:
    status = personalize.describe_dataset_import_job(
        datasetImportJobArn=job_arn)['datasetImportJob']['status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))
