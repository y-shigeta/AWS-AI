import boto3
import json
import pprint
import time
import uuid
import urllib

PATH = '/Users/yas/Desktop/VSCode-Python/AI/transcribe/'

bucket = str(uuid.uuid1())
print('bucket:', bucket)
region = 'us-east-2'
s3 = boto3.client('s3', region)
result = s3.create_bucket(
    Bucket=bucket,
    CreateBucketConfiguration={'LocationConstraint': region})

file = PATH+'scribe_file_in.mp3'
key = 'input'
s3.upload_file(file, bucket, key)

transcribe = boto3.client('transcribe', region)
job = str(uuid.uuid1())
uri = 'https://s3-'+region+'.amazonaws.com/'+bucket+'/'+key
result = transcribe.start_transcription_job(
    TranscriptionJobName=job, Media={'MediaFileUri': uri},
    MediaFormat='mp3', LanguageCode='en-US')
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

print('transcript:')
for transcript in transcripts['results']['transcripts']:
    print(transcript['transcript'])

transcribe.delete_transcription_job(TranscriptionJobName=job)
s3.delete_object(Bucket=bucket, Key=key)
s3.delete_bucket(Bucket=bucket)
