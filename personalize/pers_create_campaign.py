import boto3
import time

personalize = boto3.client('personalize')

for group in personalize.list_dataset_groups()['datasetGroups']:
    if group['name'] == 'MyGroup':
        break
group_arn = group['datasetGroupArn']

for solution in personalize.list_solutions(
        datasetGroupArn=group_arn)['solutions']:
    if solution['name'] == 'MySolution':
        break
solution_arn = solution['solutionArn']

version_arn = personalize.list_solution_versions(
    solutionArn=solution_arn
    )['solutionVersions'][0]['solutionVersionArn']

campaign_arn = personalize.create_campaign(
    name='MyCampaign', solutionVersionArn=version_arn,
    minProvisionedTPS=1)['campaignArn']
print('campaign ARN:', campaign_arn)

start = time.time()
status = ''
while status not in ['ACTIVE', 'CREATE FAILED']:
    status = personalize.describe_campaign(
        campaignArn=campaign_arn)['campaign']['status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))
