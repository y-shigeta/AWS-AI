import boto3
import time

#iam = boto3.client('iam')
#iam.delete_service_linked_role(RoleName='AWSServiceRoleForLexBots')
#iam.create_service_linked_role(AWSServiceName='lex.amazonaws.com')

lex = boto3.client('lex-models', 'us-east-1')

def createBot():
    flavor_slot_type = lex.put_slot_type(
        name='FlavorSlotType',
        enumerationValues=[
            {'value': 'Math'},
            {'value': 'English'},
            {'value': 'Programing'},
            {'value': 'Drawing'}
        ],
        valueSelectionStrategy='TOP_RESOLUTION',
        createVersion=True)
    print('slot type:', flavor_slot_type['name'])

    container_slot_type = lex.put_slot_type(
        name='ContainerSlotType',
        enumerationValues=[
            {'value': 'Masae'},
            {'value': 'Yasunori'},
            {'value': 'Kouki'},
            {'value': 'Juri'}
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
                        'content': 'Math, English, Programing or drawing?'
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
                        'content': 'Masae, Yasunori, Koki or Juri?'
                    }],
                    'maxAttempts': 3
                }
            }
        ],
        sampleUtterances=[
            '{Container} likes {Flavor} ',
            'study'
        ],
        conclusionStatement={
            'messages': [{
                'contentType': 'PlainText',
                'content': 'OK, {Container} likes {Flavor}'
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

def deleteBot():
    for bot in lex.get_bots()['bots']:
        print('bot:', bot['name'])
    for bot_alias in lex.get_bot_aliases(
            botName=bot['name'])['BotAliases']:
        lex.delete_bot_alias(
            name=bot_alias['name'], botName=bot['name'])
    while True:
        try:
            lex.delete_bot(name=bot['name'])
            break
        except Exception:
            time.sleep(1)

    for intent in lex.get_intents()['intents']:
        print('intent:', intent['name'])
        while True:
            try:
                lex.delete_intent(name=intent['name'])
                break
            except Exception:
                time.sleep(1)

    for slot_type in lex.get_slot_types()['slotTypes']:
        print('slot type:', slot_type['name'])
        while True:
            try:
                lex.delete_slot_type(name=slot_type['name'])
                break
            except Exception:
                time.sleep(1)

    iam = boto3.client('iam')
    iam.delete_service_linked_role(RoleName='AWSServiceRoleForLexBots')

if __name__ == "__main__":
    createBot()
    #deleteBot()

