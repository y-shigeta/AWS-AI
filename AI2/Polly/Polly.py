# import for translate
import boto3 
import pprint

#import for polly
import contextlib
#from pygame import mixer # Load the required library
import playsound

# Const
TEXT = "I will be back, shigeta"
PATH="/Users/yas/Desktop/VSCode-Python/AI/Polly/"
OUTPUTVOICE=PATH+"output.mp3"

polly = boto3.client('polly')
result = polly.synthesize_speech(
    Text=TEXT,OutputFormat='mp3',VoiceId="Mizuki")

# Open voice stream
with contextlib.closing(result['AudioStream']) as stream:
    with open(OUTPUTVOICE, 'wb') as voicefile:
        voicefile.write(stream.read())

# Play voice
playsound.playsound(OUTPUTVOICE, True)
