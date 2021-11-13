import boto3
import json

iam = boto3.client('iam')

role_json = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "personalize.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
role = iam.create_role(
    RoleName='PersonalizeRole',
    AssumeRolePolicyDocument=json.dumps(role_json))
print('role ARN:', role['Role']['Arn'])

policy_json = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::*"
            ]
        }
    ]
}
policy = iam.create_policy(
    PolicyName='PersonalizePolicy',
    PolicyDocument=json.dumps(policy_json))
print('policy ARN:', policy['Policy']['Arn'])

iam.attach_role_policy(
    RoleName='PersonalizeRole',
    PolicyArn=policy['Policy']['Arn'])
