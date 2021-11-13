import boto3
polly = boto3.client('polly')
with open('my_lexicon.pls', 'r', encoding='utf-8') as file:
    polly.put_lexicon(Name='MyLexicon', Content=file.read())
