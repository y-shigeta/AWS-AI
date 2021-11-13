import boto3
translate = boto3.client('translate')
translate.delete_terminology(Name='term_ja')
