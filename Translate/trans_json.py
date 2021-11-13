import boto3
import json
translate = boto3.client('translate', 'us-east-2')
with open('trans_json_in.json', 'r', encoding='utf-8') as file_in:
    reviews = json.load(file_in)
for review in reviews:
    result = translate.translate_text(
        Text=review['Text'],
        SourceLanguageCode='auto', TargetLanguageCode='ja')
    review['Text'] = result['TranslatedText']
with open('trans_json_out.json', 'w', encoding='utf-8') as file_out:
    json.dump(reviews, file_out, indent=4, ensure_ascii=False)
