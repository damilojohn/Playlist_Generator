import boto3
import json
import logging
import pickle
from io import BytesIO
from playlist_generator import PlaylistGenerator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


bucket = 'playlistgenerator'
key = 'embeddings (1).pkl'


def GetEmbeddingsFromS3():
    s3 = boto3.resource('s3')
    with BytesIO() as f:
        s3.Bucket(bucket).download_fileobj(key, f)
        f.seek(0)
        embeds = pickle.load(f)
    return embeds


logger.info('loading model....')

model = PlaylistGenerator()

logger.info('model loaded from file....')


def handler(event, _context):
    """main model prediction api"""
    try:
        input = event["body"]
        prompt = input["prompt"]
    except TypeError:
        input = json.loads(event["body"])
        prompt = input["prompt"]
    if prompt is None:
        return {'statusCode': 400, 'message': 'no input prompt was provided'}
    logger.info('downloading embeddings from s3....')
    song_embeddings = GetEmbeddingsFromS3()
    logger.info('embeddings downloaded.....')
    logger.info('starting inference....')
    prompt_embed = model.generate_embeds(prompt)
    logger.info('embeddings generated....')
    logger.info('performing semantic search ...')
    hits = model.generate_playlist(song_embeddings)
    prompt_embed = prompt_embed.tolist()
    return {
        "body": json.dumps({"embeddings": prompt_embed,
                            "hits": hits}),
        "statusCode": 200,
        'headers': {
            'Content-type': 'application/json'}
        }
