import boto3
polly = boto3.client('polly')
polly.delete_lexicon(Name='MyLexicon')
