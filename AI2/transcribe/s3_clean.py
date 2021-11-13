import boto3
import pprint
s3 = boto3.client('s3')
buckets = s3.list_buckets()
for bucket in buckets['Buckets']:
    pprint.pprint(bucket)
    name = bucket['Name']
    objects = s3.list_objects(Bucket=name)
    if 'Contents' in objects:
        for object in objects['Contents']:
            s3.delete_object(Bucket=name, Key=object['Key'])
    s3.delete_bucket(Bucket=name)
