import boto3
translate = boto3.client('translate')
text = "I'll send you an email later."
result = translate.translate_text(
    Text=text, SourceLanguageCode='en', TargetLanguageCode='ja')
print(result['TranslatedText'])
