import requests 
import boto3 
import json 
import app 

model = app.sentence_transformer

def handler(event,_context):
    """main prediction api"""
    prompt = event['prompt']
    if event is None:
        return {'statusCode':400,'message':'no input prompt was provided'}
    print('starting inference...')
    output = model(prompt)
    print('embeddings created ')
    return {"body": json.dumps({"embeddings":output})}   
            
    
    