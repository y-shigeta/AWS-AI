import boto3
import time

personalize = boto3.client('personalize')

for group in personalize.list_dataset_groups()['datasetGroups']:
    if group['name'] == 'MyGroup':
        break
group_arn = group['datasetGroupArn']

solution_arn = personalize.create_solution(
    name='MySolution', datasetGroupArn=group_arn,
    performAutoML=True)['solutionArn']
print('solution ARN:', solution_arn)

start = time.time()
status = ''
while status not in ['ACTIVE', 'CREATE FAILED']:
    status = personalize.describe_solution(
        solutionArn=solution_arn)['solution']['status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))

version_arn = personalize.create_solution_version(
    solutionArn=solution_arn)['solutionVersionArn']
print('solution version ARN:', version_arn)

start = time.time()
status = ''
while status not in ['ACTIVE', 'CREATE FAILED']:
    status = personalize.describe_solution_version(
        solutionVersionArn=version_arn)['solutionVersion']['status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))
