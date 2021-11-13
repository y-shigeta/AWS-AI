import boto3
import json

iam = boto3.client('iam')

role_json = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "forecast.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

role = iam.create_role(
    RoleName='ForecastRole',
    AssumeRolePolicyDocument=json.dumps(role_json))
print('role ARN:', role['Role']['Arn'])

policy_json = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3:PutObject"
            ],
            "Effect":"Allow",
            "Resource":[
                "arn:aws:s3:::*"
            ]
        }
    ]
}

policy = iam.create_policy(
    PolicyName='ForecastPolicy',
    PolicyDocument=json.dumps(policy_json))
print('policy ARN:', policy['Policy']['Arn'])

iam.attach_role_policy(
    RoleName='ForecastRole',
    PolicyArn=policy['Policy']['Arn'])
