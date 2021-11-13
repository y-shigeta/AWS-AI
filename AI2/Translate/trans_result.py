import boto3
import pprint
translate = boto3.client('translate')
text = 'あとでメールを送ります。'
result = translate.translate_text(
    Text=text, SourceLanguageCode='ja', TargetLanguageCode='en')
pprint.pprint(result)
