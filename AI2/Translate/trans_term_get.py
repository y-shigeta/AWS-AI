import boto3
import pprint
translate = boto3.client('translate')
result = translate.get_terminology(
    Name='term_ja', TerminologyDataFormat='CSV')
pprint.pprint(result)
