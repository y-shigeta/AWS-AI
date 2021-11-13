import boto3
import sys

if len(sys.argv) != 2:
    print('python', sys.argv[0], 'user-id')
    exit()

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

for group in personalize.list_dataset_groups()['datasetGroups']:
    if group['name'] == 'MyGroup':
        break
group_arn = group['datasetGroupArn']

for solution in personalize.list_solutions(
        datasetGroupArn=group_arn)['solutions']:
    if solution['name'] == 'MySolution':
        break
solution_arn = solution['solutionArn']

for campaign in personalize.list_campaigns(
        solutionArn=solution_arn)['campaigns']:
    if campaign['name'] == 'MyCampaign':
        break
campaign_arn = campaign['campaignArn']

result = personalize_runtime.get_recommendations(
    campaignArn=campaign_arn, userId=sys.argv[1])

with open('item.txt', 'r') as file:
    name = list(file)

for rank, item in enumerate(result['itemList'], 1):
    print('{:2} {}'.format(rank, name[int(item['itemId'])]), end='')
