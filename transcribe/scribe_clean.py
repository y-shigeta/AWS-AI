import boto3
import pprint
region = 'us-east-2'
transcribe = boto3.client('transcribe', region)
print('list_transcription_jobs:')
jobs = transcribe.list_transcription_jobs()
for job in jobs['TranscriptionJobSummaries']:
    pprint.pprint(job)
    if job['TranscriptionJobStatus'] != 'IN_PROGRESS':
        transcribe.delete_transcription_job(
            TranscriptionJobName=job['TranscriptionJobName'])
