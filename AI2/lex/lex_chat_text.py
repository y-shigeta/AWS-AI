import boto3
import uuid
lex_runtime = boto3.client('lex-runtime', 'us-east-2')
user = str(uuid.uuid1())
state = ''
while state != 'Fulfilled':
    result = lex_runtime.post_text(
        botName='MyBot', botAlias='MyBotAlias',
        userId=user, inputText=input('You: '))
    print('Bot:', result['message'])
    state = result['dialogState']
print()
print('Flavor   :', result['slots']['Flavor'])
print('Container:', result['slots']['Container'])
