import boto3
import contextlib
import os
polly = boto3.client('polly')
text = 'P2Pは複数の端末が対等な立場で通信する方式です。'
result = polly.synthesize_speech(
    Text=text, OutputFormat='mp3', VoiceId='Mizuki',
    LexiconNames=['MyLexicon'])
path = 'polly_lexicon_enabled.mp3'
with contextlib.closing(result['AudioStream']) as stream:
    with open(path, 'wb') as file:
        file.write(stream.read())
if os.name == 'nt':
    os.startfile(path)
