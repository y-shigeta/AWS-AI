import boto3
import json
import sys

if len(sys.argv) != 2:
    print('python', sys.argv[0], 'image')
    exit()

rekognition = boto3.client('rekognition')
with open(sys.argv[1], 'rb') as file:
    result = rekognition.detect_faces(Image={'Bytes': file.read()})
    print(json.dumps(result, indent=4))
