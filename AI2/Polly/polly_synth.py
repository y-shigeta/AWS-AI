import boto3
import contextlib
import os
polly = boto3.client('polly')
text = 'こんにちは！音声合成を使ったプログラムを一緒に作りましょう。'
result = polly.synthesize_speech(
    Text=text, OutputFormat='mp3', VoiceId='Mizuki')
path = 'polly_synth.mp3'
with contextlib.closing(result['AudioStream']) as stream:
    with open(path, 'wb') as file:
        file.write(stream.read())
if os.name == 'nt':
    os.startfile(path)
