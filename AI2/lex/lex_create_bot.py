import boto3
import time

#iam = boto3.client('iam')
#iam.delete_service_linked_role(RoleName='AWSServiceRoleForLexBots')
#iam.create_service_linked_role(AWSServiceName='lex.amazonaws.com')

lex = boto3.client('lex-models', 'us-east-1')

flavor_slot_type = lex.put_slot_type(
    name='FlavorSlotType',
    enumerationValues=[
        {'value': 'vanilla'},
        {'value': 'chocolate', 'synonyms': ['choc']},
        {'value': 'strawberry', 'synonyms': ['berry']}
    ],
    valueSelectionStrategy='TOP_RESOLUTION',
    createVersion=True)
print('slot type:', flavor_slot_type['name'])

container_slot_type = lex.put_slot_type(
    name='ContainerSlotType',
    enumerationValues=[
        {'value': 'corn'},
        {'value': 'cup'}
    ],
    valueSelectionStrategy='TOP_RESOLUTION',
    createVersion=True)
print('slot type:', container_slot_type['name'])

intent = lex.put_intent(
    name='OrderIntent',
    slots=[
        {
            'name': 'Flavor',
            'slotConstraint': 'Required',
            'slotType': 'FlavorSlotType',
            'slotTypeVersion': '1',
            'valueElicitationPrompt': {
                'messages': [{
                    'contentType': 'PlainText',
                    'content': 'Vanilla, chocolate or strawberry?'
                }],
                'maxAttempts': 3
            }
        },
        {
            'name': 'Container',
            'slotConstraint': 'Required',
            'slotType': 'ContainerSlotType',
            'slotTypeVersion': '1',
            'valueElicitationPrompt': {
                'messages': [{
                    'contentType': 'PlainText',
                    'content': 'Corn or cup?'
                }],
                'maxAttempts': 3
            }
        }
    ],
    sampleUtterances=[
        'I want {Flavor} ice cream in {Container}',
        '{Flavor} ice cream {Container}',
        'ice cream'
    ],
    conclusionStatement={
        'messages': [{
            'contentType': 'PlainText',
            'content': 'OK, {Flavor} ice cream in {Container}'
        }],
    },
    fulfillmentActivity={'type': 'ReturnIntent'},
    createVersion=True)
print('intent:', intent['name'])

bot = lex.put_bot(
    name='MyBot', locale='en-US', childDirected=False,
    intents=[
        {
            'intentName': 'OrderIntent',
            'intentVersion': '1'
        }
    ],
    abortStatement={
        'messages': [
            {
                'contentType': 'PlainText',
                'content': 'Please try again.'
            }
        ]
    },
    voiceId='Joanna',
    createVersion=True)
print('bot:', bot['name'])

start = time.time()
status = ''
while status not in ['READY', 'FAILED']:
    status = lex.get_bot(name='MyBot', versionOrAlias='1')['status']
    time.sleep(10)
    print('{:7.2f} {}'.format(time.time()-start, status))
if status == 'FAILED':
    print(lex.get_bot(
        name='MyBot', versionOrAlias='1')['failureReason'])

bot_alias = lex.put_bot_alias(
    name='MyBotAlias', botName='MyBot', botVersion='1')
print('bot alias:', bot_alias['name'])
