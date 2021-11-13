import boto3
import contextlib
import os
polly = boto3.client('polly')
text = 'Hello everyone! Welcome to the Programming World Report.'
result = polly.synthesize_speech(
    Text=text, OutputFormat='mp3', VoiceId='Joanna')
path = 'polly_standard.mp3'
with contextlib.closing(result['AudioStream']) as stream:
    with open(path, 'wb') as file:
        file.write(stream.read())
if os.name == 'nt':
    os.startfile(path)
