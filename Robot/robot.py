# import for translate
import boto3 
import pprint
import contextlib
import time
import uuid
import urllib
import sys
import os
import time
import json
import pyaudio
import wave
#import matplotlib.pyplot as plt
#import numpy as np

# Const
#TEXT = "I will be back, shigeta"
#WAVFILE="voicerecord.wav"
PATH="/Users/yas/Desktop/VSCode-Python/AI/Robot/"
region = 'us-east-2'
BUCKET = "infra-myraspberrypi"
ENV = "MAC"

"""
def MakeWavFile(FileName = "sample.wav", Record_Seconds = 2, save = True):
    chunk = 1024
    FORMAT = pyaudio.paInt16
    
    CHANNELS = 1 #モノラル
    RATE = 44100 #サンプルレート（録音の音質）
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    
    #レコード開始
    print("Now Recording...")
    all = []
    for i in range(0, int(RATE / chunk * Record_Seconds)):
        data = stream.read(chunk) #音声を読み取って、
        all.append(data) #データを追加
    
    #レコード終了
    print("Finished Recording.")
    
    stream.close()
    p.terminate()
    
    #録音したデータを配列に変換
    #data = ''.join(all) #Python2用
    data = b"".join(all) #Python3用
    result = np.frombuffer(data,dtype="int16") / float(2**15)
    plt.plot(result)
    plt.show()
    
    if(save): #保存するか？
        wavFile = wave.open(FileName, 'wb')
        wavFile.setnchannels(CHANNELS)
        wavFile.setsampwidth(p.get_sample_size(FORMAT))
        wavFile.setframerate(RATE)
        wavFile.writeframes(b''.join(all)) #Python2 用
        #wavFile.writeframes(b"".join(all)) #Python3用
        wavFile.close()
    
def ReadWavFile(FileName = "sample.wav"):
    try:
        wr = wave.open(FileName, "r")
    except FileNotFoundError: #ファイルが存在しなかった場合
        print("[Error 404] No such file or directory: " + FileName)
        return 0
    data = wr.readframes(wr.getnframes())
    wr.close()
    x = np.frombuffer(data, dtype="int16") / float(2**15)

    plt.figure(figsize=(15,3))
    plt.plot(x)
    plt.show()
    
    x = np.fft.fft(np.frombuffer(data, dtype="int16"))
    plt.figure(figsize=(15,3))
    plt.plot(x.real[:int(len(x)/2)])
    plt.show()
"""

def PlayWavFie(Filename):
    #wavファイルを再生
    try:
        wf = wave.open(Filename, "r")
    except FileNotFoundError: #ファイルが存在しなかった場合
        print("[Error 404] No such file or directory: " + Filename)
        return 0
        
    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()

def doRecord(sec):  
    wavfile=str(uuid.uuid1())+".wav"
#    MakeWavFile(FileName = "sample.wav", Record_Seconds = 2, save = True)
#    os.system("sudo arecord -D plughw:1,0 -d "+str(sec)+" "+PATH+WAVFILE)
#    os.system("rec --encoding signed-integer --bits 16 --channels 1 --rate 16000 "+WAVFILE)
    if ENV == "MAC":
        os.system("rec -c 1 -r 16k -b 16 "+PATH+wavfile+" trim 0 "+str(sec))
    else:
        os.system("sudo arecord -D plughw:1,0 -d "+str(sec)+" "+PATH+wavfile)

    return wavfile

"""
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #サンプリングレート、マイク性能に依存
    RATE = 44100
    #録音時間
    #RECORD_SECONDS = input('Please input recoding time>>>')
    RECORD_SECONDS = 2
    
    #pyaudio
    p = pyaudio.PyAudio()

    #マイク0番を設定
    input_device_index = 0
    #マイクからデータ取得
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    all = []
    for i in range(0, RATE / chunk * RECORD_SECONDS):
        data = stream.read(chunk)
        all.append(data)

    stream.close()
    data = ''.join(all)
    out = wave.open(WAVFILE,'w')
    out.setnchannels(1) #mono
    out.setsampwidth(2) #16bits
    out.setframerate(RATE)
    out.writeframes(data)
    out.close()
    
    p.terminate()
"""

# get image file name to extract document and return 
def getText(image):
    textract = boto3.client('textract', 'us-east-2')
    #IMAGE='novel.jpg'
    data = ""
    # read image to get text
    with open(image, 'rb') as file:
        result = textract.analyze_document(
            Document={'Bytes': file.read()},
            FeatureTypes=['TABLES', 'FORMS'])
        print(json.dumps(result, indent=4))
    for key in result['Blocks']:
        if key['BlockType'] != "PAGE":
            print(key['Text'])
            data = data +" "+ key['Text']

    return data

# get text and check emotion. return emotion with its percentage.
def CheckEmotion(text, lang):
    comprehend = boto3.client('comprehend', 'us-east-2')
    result = comprehend.detect_sentiment(Text=text, LanguageCode=lang)
    print(json.dumps(result, indent=4))
    score = 0
    if result['SentimentScore']['Positive'] > 0.25:
        score = round( result['SentimentScore']['Positive'] * 100)
        return ("Positive", score)
    elif result['SentimentScore']['Negative'] > 0.25:
        score = round( result['SentimentScore']['Negative'] * 100)
        return ("Negative", score)
    elif result['SentimentScore']['Neutral'] > 0.25:
        score = round( result['SentimentScore']['Neutral'] * 100)
        return ("Neutral", score)
    else:
        score = round( result['SentimentScore']['Mixed'] * 100)
        return ("Mixed", score)

# get wav file to transform to text
def doTransfrom(wavfile):
    #bucket = str(uuid.uuid1())
    #s3 = boto3.client('s3')
    s3 = boto3.resource('s3')
    #result = s3.create_bucket(Bucket=bucket,CreateBucketConfiguration={'LocationConstraint': region})
    bucket = s3.Bucket(BUCKET)

    key = 'input'
    bucket.upload_file(PATH+wavfile, key)

    job = str(uuid.uuid1())
    uri = 'https://s3-'+region+'.amazonaws.com/'+BUCKET+'/'+key
    transcribe = boto3.client('transcribe', region)
    result = transcribe.start_transcription_job(
        TranscriptionJobName=job, Media={'MediaFileUri': uri},
        MediaFormat='wav', LanguageCode='en-US')
    print('start_transcription_job:')
    pprint.pprint(result)

    start = time.time()
    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=job)
        status = result['TranscriptionJob']['TranscriptionJobStatus']
        if status != 'IN_PROGRESS':
            break
        time.sleep(10)
        print('time:', time.time()-start)
    print('get_transcription_job:')
    pprint.pprint(result)

    uri = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print('uri:', uri)
    with urllib.request.urlopen(uri) as file_in:
        transcripts = json.load(file_in)
    with open('scribe_file_out.json', 'w', encoding='utf-8') as file_out:
        json.dump(transcripts, file_out, indent=4)

    ans = ""
    print('transcript:')
    for transcript in transcripts['results']['transcripts']:
        print(transcript['transcript'])
        ans = transcript['transcript']

    transcribe.delete_transcription_job(TranscriptionJobName=job)
    #bucket.delete_object(Key=key)
    #s3.delete_bucket(Bucket=bucket)

    return ans

def doTranslate(text):
    translate = boto3.client('translate')    
    # import terms
    """
    TERMFILE = "term_ja"
    with open(PATH+TERMFILE+'.csv', 'rb') as file:
        translate.import_terminology(
            Name=TERMFILE,
            MergeStrategy='OVERWRITE',
            TerminologyData={'File': file.read(), 'Format':'CSV'}
        )
    """

    # Translate using the term
    #result = translate.translate_text(Text=jatext, SourceLanguageCode='ja',TargetLanguageCode='en',TerminologyNames=[TERMFILE])
    result = translate.translate_text(Text=text, SourceLanguageCode='en',TargetLanguageCode='ja')
    print(result['TranslatedText'])
    return result['TranslatedText']

    
def doSpeak(text):
    # Polly
    OUTPUTVOICE=PATH+"doSpeak.mp3"
    result = None
    polly = boto3.client('polly')
    result = polly.synthesize_speech(Text=text,OutputFormat='mp3',VoiceId="Mizuki")
    
    # Open voice stream
    with contextlib.closing(result['AudioStream']) as stream:
        with open(OUTPUTVOICE, 'wb') as voicefile:
            voicefile.write(stream.read())
    
    # Play voice
    #PlayWavFie(Filename=OUTPUTVOICE)
    if ENV == "MAC":
        os.system("afplay "+OUTPUTVOICE)
    else:
        os.system("aplay "+OUTPUTVOICE)
    """
    mixer.init()
    mixer.music.load(OUTPUTVOICE)
    mixer.music.play()
    """

def takeCamera():
    image=PATH+'novel.jpg'
    if ENV != 'MAC':
#       import camera
#        image=camera.takeCamera()
        print(image)
    return image

# Get Enlish voice and translate it to Japanese. After that, spleak it.
def RobotTranlate():
    # Record 5 secs
    doSpeak('英語で2秒以内に話かけてください')
    #os.system("aplay "+PATH+"startdialog.mp3")
    wavfile = doRecord(2)

    # Transform WAV file to Text file
    entext = doTransfrom(wavfile)
    doSpeak('あなたが話した英語はこちらですね')
    doSpeak(entext)
    
    # Translate english to japanese
    doSpeak('これから翻訳します')
    jptext = doTranslate(entext)
    doSpeak(jptext)

# take shot with camera and transform the string in the image. After that, speak.
def RobotOCR():
    image = takeCamera()
    text = getText(image)
    doSpeak(text)
    
def RobotChatVoice():
    lex_runtime = boto3.client('lex-runtime', 'us-east-1')
    user = str(uuid.uuid1())
    count = 0
    state = ''
    doSpeak("私はシゲクサです。家族の誰がどんなことが好きか英語で当ててください。")
    while state != 'Fulfilled':
    #    wav = input('Wav: ')
        wav=doRecord(3)
        #wav='choc_ice_corn.wav'
        with open(PATH+wav, 'rb') as file:
            result = lex_runtime.post_content(
                botName='MyBot', botAlias='MyBotAlias',
                userId=user, accept='audio/mpeg',
                contentType='audio/l16; rate=16000; channels=1',
                inputStream=file.read())
        print('Bot:', result['message'])
        resfile = PATH+'bot{}.mp3'.format(count)
        count += 1
        if count > 4:
            doSpeak("失敗しすぎですね")
            break
        with contextlib.closing(result['audioStream']) as stream:
            with open(resfile, 'wb') as file:
                file.write(stream.read())
        if ENV == "MAC":
            os.system("afplay "+resfile)
        else:
            os.system("aplay "+resfile)
        state = result['dialogState']
    if state == 'Fulfilled':
        print('Flavor   :', result['slots']['Flavor'])
        print('Container:', result['slots']['Container'])

if __name__ == '__main__':
    #RobotOCR()
    #RobotTranlate()
    doSpeak('こうきはコロコロを買ってもらって嬉しい。そろそろお風呂に入らないといけない')
    #RobotChatVoice()
