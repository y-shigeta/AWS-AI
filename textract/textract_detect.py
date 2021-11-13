import boto3
import json
import sys
from PIL import Image

if len(sys.argv) != 2:
    print('python', sys.argv[0], 'image')
    exit()

textract = boto3.client('textract', 'us-east-2')
with open(sys.argv[1], 'rb') as file:
    result = textract.detect_document_text(
        Document={'Bytes': file.read()})
    print(json.dumps(result, indent=4))

image_in = Image.open(sys.argv[1])
w, h = image_in.size
image_out = Image.new('RGB', (w, h), (200, 200, 200))
for block in result['Blocks']:
    if block['BlockType'] == 'LINE':
        box = block['Geometry']['BoundingBox']
        left = int(box['Left']*w)
        top = int(box['Top']*h)
        right = left+int(box['Width']*w)
        bottom = top+int(box['Height']*h)
        image_out.paste(
            image_in.crop((left, top, right, bottom)), (left, top))
        print(block['Text']),
image_out.save('detect_'+sys.argv[1])
image_out.show()
