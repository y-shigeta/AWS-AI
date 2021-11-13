import boto3

personalize = boto3.client('personalize')

for campaign in personalize.list_campaigns()['campaigns']:
    campaign_arn = campaign['campaignArn']
    print('campaign ARN:', campaign_arn)
    personalize.delete_campaign(campaignArn=campaign_arn)
