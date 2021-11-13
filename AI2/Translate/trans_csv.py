import boto3
import csv
translate = boto3.client('translate', 'us-east-2')
with open('trans_csv_in.csv', 'r', encoding='utf-8') as file_in:
    with open('trans_csv_out.csv', 'w', encoding='utf-8',
              newline='') as file_out:
        writer = csv.writer(file_out)
        for row in csv.reader(file_in):
            result = translate.translate_text(
                Text=row[2],
                SourceLanguageCode='auto', TargetLanguageCode='ja')
            row[2] = result['TranslatedText']
            writer.writerow(row)
