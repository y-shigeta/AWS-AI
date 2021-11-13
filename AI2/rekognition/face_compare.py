import boto3
import json
import sys
from PIL import Image

if len(sys.argv) != 3:
    print('python', sys.argv[0], 'source-image', 'target-image')
    exit()

rekognition = boto3.client('rekognition')
with open(sys.argv[1], 'rb') as source:
    with open(sys.argv[2], 'rb') as target:
        result = rekognition.compare_faces(
            SourceImage={'Bytes': source.read()},
            TargetImage={'Bytes': target.read()})
        print(json.dumps(result, indent=4))

image_in = Image.open(sys.argv[2])
w, h = image_in.size
image_out = Image.new('RGB', (w, h), (200, 200, 200))
for face in result['FaceMatches']:
    box = face['Face']['BoundingBox']
    left = int(box['Left']*w)
    top = int(box['Top']*h)
    right = left+int(box['Width']*w)
    bottom = top+int(box['Height']*h)
    image_out.paste(
        image_in.crop((left, top, right, bottom)),
        (left, top))
image_out.save('compare_'+sys.argv[2])
image_out.show()
