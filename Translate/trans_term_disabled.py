import boto3
translate = boto3.client('translate')
text = 'ひぐぺん工房の新しい本が秀和システムから出ます。'
result = translate.translate_text(
    Text=text, SourceLanguageCode='ja', TargetLanguageCode='en')
print(result['TranslatedText'])
