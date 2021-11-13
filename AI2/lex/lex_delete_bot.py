import boto3
import time

lex = boto3.client('lex-models', 'us-east-1')

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
