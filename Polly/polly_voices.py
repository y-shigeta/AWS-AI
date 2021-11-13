import boto3
import pprint
polly = boto3.client('polly')
result = polly.describe_voices()
pprint.pprint(result)
