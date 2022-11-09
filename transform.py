#Importing the necesssary libraries
from extract import create_dataframe
from requests_html import HTMLSession
import yaml
#This starts an request session 
def start_session():
    session=HTMLSession()
    return session

#This function gets the lyrics from the lyricsgenius api
def get_from_genius(url):
    session=start_session()
    get_raw=session.get(url)
    with open('config.yaml','r') as get_xpath:
        lyrics_xpath=yaml.safe_load(get_xpath)['lyric_xpath']
    get_lyrics=get_raw.html.find(lyrics_xpath)
    if get_lyrics==[]:
        return []
    else:
        return get_lyrics[0].text[:2800]

#This function cleans the dataframe and transforms it for the lyricsgenius api and the azlyrics api
'''Since we are using a totally different api for the lyrics, the function below might take a while to run'''
def transform(df):
    df['cleaned_song_name']=df['song_name'].apply(lambda x:x.split('(')[0])
    df['artist_cleaned']=df['artist'].apply(lambda x:x.lower())
    df['cleaned_song_name']=df['cleaned_song_name'].apply(lambda x:x.lower())
    df['cleaned_song_name']=df['cleaned_song_name'].apply(lambda x:x.strip())

    df['cleaned_song_name']=df['cleaned_song_name'].str.replace(' ','-')
    df['artist_cleaned']=df['artist_cleaned'].str.replace(' ','-')

    df['for_lyrics']='https://genius.com/'+df['artist_cleaned']+'-'+df['cleaned_song_name']+'-lyrics'

    df=df.drop([2,3])
    df['for_lyrics']=df['for_lyrics'].apply(get_from_genius)
    df=df[['id','album','artist','song_name','image','url','for_lyrics']]
    return df
