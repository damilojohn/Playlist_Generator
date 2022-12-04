import pandas as pd
import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials
file_name='./config.yaml'

#This authenticates the user and grants access to the Spotify's api.
def authenticate_user(path):
    with open(path,'rb') as file:
        configuration_keys=yaml.safe_load(file)['config_keys']
        client_id=configuration_keys['client_id']
        secret_id=configuration_keys['secret_id']
    auth_manager = SpotifyClientCredentials(client_id=client_id,client_secret=secret_id)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

#The function below creates a dataframe of artists names, top tracks, album names and general metadata from the api
def create_dataframe():
    with open(file_name,'r') as read_artist_config:
        artist_config=yaml.safe_load(read_artist_config)['artist_id_config']
    df=pd.DataFrame(columns=['id','album','artist','song_name','image','url','lyrics'])
    idd=[]
    album=[]
    artist_list=[]
    song_name=[]
    image=[]
    url=[]
    for i in artist_config.items():
        for k in authenticate_user(file_name).artist_top_tracks(i[1])['tracks']:
            idd.append(i[1])
            album.append(k['album']['name'])
            artist_list.append(i[0])
            song_name.append(k['name'])
            url.append(k['external_urls']['spotify'])
            for l in k['album']['images']:
                image.append(l['url'])
    df['id']=pd.Series(idd)
    df['album']=pd.Series(album)
    df['artist']=pd.Series(artist_list)
    df['song_name']=pd.Series(song_name)
    df['image']=pd.Series(image)
    df['url']=pd.Series(url)
    df['lyrics']=''
    return df

