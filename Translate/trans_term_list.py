import boto3
import pprint
translate = boto3.client('translate')
result = translate.list_terminologies()
pprint.pprint(result)
