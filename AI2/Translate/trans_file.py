import boto3
translate = boto3.client('translate')
with open('trans_file_in.txt', 'r', encoding='utf-8') as file_in:
    with open('trans_file_out.txt', 'w', encoding='utf-8') as file_out:
        for text in file_in:
            if text != '\n':
                result = translate.translate_text(
                    Text=text,
                    SourceLanguageCode='ja', TargetLanguageCode='en',
                    TerminologyNames=['term_ja'])
                file_out.write(result['TranslatedText'])
            file_out.write('\n')
