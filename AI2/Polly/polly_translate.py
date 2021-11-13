import boto3
import contextlib
import os
translate = boto3.client('translate')
polly = boto3.client('polly')
text_ja = '一番近い駅までの道を教えてください。'
result = translate.translate_text(
    Text=text_ja, SourceLanguageCode='ja', TargetLanguageCode='en')
text_en = result['TranslatedText']
print(text_en)
result = polly.synthesize_speech(
    Text=text_en, OutputFormat='mp3', VoiceId='Joanna')
path = 'polly_translate.mp3'
with contextlib.closing(result['AudioStream']) as stream:
    with open(path, 'wb') as file:
        file.write(stream.read())
if os.name == 'nt':
    os.startfile(path)
