import pyspark
from pyspark.sql import SparkSession,Row
from requests_html import HTMLSession
import numpy as np
from pyspark.sql.functions import col,lit,explode,array,udf,concat,struct
from pyspark.sql.types import StructType,StructField,StringType,ArrayType,List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yaml
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
    
#Creating a spark session
def spark():
    create_spark=SparkSession.builder.appName('Spotify and Genius API with Pyspark').getOrCreate()
    return create_spark

#Creating a dataframe
def create_dataframe():
    emp_RDD = spark().sparkContext.emptyRDD()
 
    columns = StructType([StructField('id',
                                    StringType(), True),
                        StructField('album',
                                    StringType(), True),
                        StructField('artist',
                                    StringType(), True),
                        StructField('song_name',
                                    StringType(), True),
                        StructField('image',
                                    StringType(), True),
                        StructField('url',
                                    StringType(), True)])
    
    df = spark().createDataFrame(data = emp_RDD,
                            schema = columns)
    with open(file_name,'r') as read_artist_config:
        artist_config=yaml.safe_load(read_artist_config)['artist_id_config']
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
    image=image[::3]
    rows=[idd,album,artist_list,song_name,image,url]
    rows_mod=np.ravel(rows)
    emp=[]
    for j in range(100):
        for i in rows:
            emp.append(i[j])
    new_emp=[]
    start=0
    end=6
    while end<601:
        new_emp.append(emp[start:end])
        start+=6
        end+=6
    main_df=spark().createDataFrame(data=new_emp,schema=columns)
    return main_df

