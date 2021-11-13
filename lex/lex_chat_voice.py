import boto3
import contextlib
import os
import uuid
lex_runtime = boto3.client('lex-runtime', 'us-east-1')
user = str(uuid.uuid1())
count = 0
state = ''
PATH='/Users/yas/Desktop/VSCode-Python/AI/lex/'
while state != 'Fulfilled':
#    wav = input('Wav: ')
    wav="choc_ice_corn"
    with open(PATH+wav+'.wav', 'rb') as file:
        result = lex_runtime.post_content(
            botName='MyBot', botAlias='MyBotAlias',
            userId=user, accept='audio/mpeg',
            contentType='audio/l16; rate=16000; channels=1',
            inputStream=file.read())
    print('Bot:', result['message'])
    path = 'bot{}.mp3'.format(count)
    count += 1
    with contextlib.closing(result['audioStream']) as stream:
        with open(path, 'wb') as file:
            file.write(stream.read())
    if os.name == 'nt':
        os.startfile(path)
    state = result['dialogState']
print()
print('Flavor   :', result['slots']['Flavor'])
print('Container:', result['slots']['Container'])
