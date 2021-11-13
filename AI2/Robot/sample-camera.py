import boto3
import json
import sys
import contextlib
import os
import robot

PATH='/Users/yas/Desktop/VSCode-Python/AI/Robot/'
IMAGE='novel.jpg'
ENV='MAC'

def getText():
    textract = boto3.client('textract', 'us-east-2')
    data = ""
    # read image to get text
    with open(PATH+IMAGE, 'rb') as file:
        result = textract.analyze_document(
            Document={'Bytes': file.read()},
            FeatureTypes=['TABLES', 'FORMS'])
        print(json.dumps(result, indent=4))
    for key in result['Blocks']:
        if key['BlockType'] != "PAGE":
            print(key['Text'])
            data = data +" "+ key['Text']

    return data

def CheckEmotion(data, lang):
    comprehend = boto3.client('comprehend', 'us-east-2')
    result = comprehend.detect_sentiment(Text=data, LanguageCode=lang)
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


if __name__ == "__main__":
    data = getText()
    (emotion, data) = CheckEmotion(data, 'en')
    data = round(data * 100)
    emotiondata = "You are "+emotion+" "+str(data)+"%"
    jpdata=robot.doTranslate(data)
    robot.doSpeak(jpdata)
