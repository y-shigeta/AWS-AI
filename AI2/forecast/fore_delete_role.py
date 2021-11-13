import boto3

iam = boto3.client('iam')

for policy in iam.list_policies()['Policies']:
    if policy['PolicyName'] == 'ForecastPolicy':
        break
policy_arn = policy['Arn']
print('policy ARN:', policy_arn)

iam.detach_role_policy(
    RoleName='ForecastRole', PolicyArn=policy_arn)
iam.delete_policy(PolicyArn=policy_arn)
iam.delete_role(RoleName='ForecastRole')
