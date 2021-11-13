# import for translate
import boto3 
import pprint

#import for polly
import contextlib
from pygame import mixer # Load the required library

translate = boto3.client('translate')

# Const
TEXT = "I will be back, shigeta"
PATH="/Users/yas/Desktop/VSCode-Python/AI/Translate/"
TERMFILE = "term_ja"
INPUTFILE="input.txt"
OUTPUTFILE="output.txt"

# import terms
print(PATH+TERMFILE)
with open(PATH+TERMFILE+'.csv', 'rb') as file:
    translate.import_terminology(
        Name=TERMFILE,
        MergeStrategy='OVERWRITE',
        TerminologyData={'File': file.read(), 'Format':'CSV'}
    )

# Translate using the term
result = translate.translate_text(
    Text=TEXT, SourceLanguageCode='en',TargetLanguageCode='ja',TerminologyNames=[TERMFILE]
)
print(result['TranslatedText'])
pprint.pprint(result)

# get list of terms
result = translate.list_terminologies()
pprint.pprint(result)

# Open file to translate for input and output
with open(PATH+INPUTFILE, 'r', encoding='utf-8') as file_in:
    with open(PATH+OUTPUTFILE, 'w', encoding='utf-8') as file_out:
        for inputline in file_in:
            # check string exists or not
            if inputline != '¥n':
                result = translate.translate_text(
                    Text=inputline, SourceLanguageCode='en',TargetLanguageCode='ja',TerminologyNames=[TERMFILE])
                file_out.write(result['TranslatedText'])
            file_out.write('¥n')

# Polly
OUTPUTVOICE=PATH+"output.mp3"

polly = boto3.client('polly')
result = polly.synthesize_speech(
    Text=TEXT,OutputFormat='mp3',VoiceId="Mizuki")

# Open voice stream
with contextlib.closing(result['AudioStream']) as stream:
    with open(OUTPUTVOICE, 'wb') as voicefile:
        voicefile.write(stream.read())

# Play voice
mixer.init()
mixer.music.load(OUTPUTVOICE)
mixer.music.play()


