import boto3
import contextlib
import os
polly = boto3.client('polly', 'us-east-1')
text = '''
<speak>
<amazon:domain name="news">
Hello everyone! Welcome to the Programming World Report.
</amazon:domain>
</speak>
'''
result = polly.synthesize_speech(
    Text=text, OutputFormat='mp3', VoiceId='Joanna',
    Engine='neural', TextType='ssml')
path = 'polly_news.mp3'
with contextlib.closing(result['AudioStream']) as stream:
    with open(path, 'wb') as file:
        file.write(stream.read())
if os.name == 'nt':
    os.startfile(path)
