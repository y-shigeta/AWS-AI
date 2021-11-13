import boto3
import csv
import json
import sys

if len(sys.argv) != 2:
    print('python', sys.argv[0], 'image')
    exit()

textract = boto3.client('textract', 'us-east-2')
with open(sys.argv[1], 'rb') as file:
    result = textract.analyze_document(
        Document={'Bytes': file.read()},
        FeatureTypes=['TABLES', 'FORMS'])
    print(json.dumps(result, indent=4))

text = {}
for block in result['Blocks']:
    if 'Text' in block:
        text[block['Id']] = block['Text']

cell = {}
for block in result['Blocks']:
    if block['BlockType'] == 'CELL':
        row = int(block['RowIndex'])-1
        column = int(block['ColumnIndex'])-1
        cell[(row, column)] = ''
        if 'Relationships' in block:
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for id in relationship['Ids']:
                        if id in text:
                            cell[(row, column)] += text[id]+' '

for row in range(8):
    for column in range(4):
        if (row, column) in cell:
            print('{:20}'.format(cell[(row, column)]), end='')
    print()
