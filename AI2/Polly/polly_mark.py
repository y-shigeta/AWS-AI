import boto3
import contextlib
polly = boto3.client('polly')
text = 'スピーチマークを出力してみます。'
result = polly.synthesize_speech(
    Text=text, OutputFormat='json', VoiceId='Mizuki',
    SpeechMarkTypes=['sentence', 'word', 'viseme'])
path = 'polly_mark.txt'
with contextlib.closing(result['AudioStream']) as stream:
    with open(path, 'wb') as file:
        file.write(stream.read())
