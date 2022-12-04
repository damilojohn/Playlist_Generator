from extract import create_dataframe,spark
from pyspark.sql.functions import udf,lit,concat,col
from pyspark.sql.types import StringType
from requests_html import HTMLSession

def trans_song(x):
    y=x.split('(')[0]
    z=y.lower()
    k=z.strip()
    i=k.replace(' ','-')
    return i
def artist_cleaned(x):
    y=x.lower()
    z=y.replace(' ','-')
    return z
def get_from_genius(i):
    session=HTMLSession()
    r=session.get(i)
    rr=r.html.find('div.Lyrics__Container-sc-1ynbvzw-6')
    if rr==[]:
        return []
    else:
        return rr[0].text[:2800]
trans_song_trans=udf(lambda x:trans_song(x))
artist_trans=udf(lambda x:artist_cleaned(x))
lyrics_trans=udf(lambda x:get_from_genius(x))

def transform_df(df):
    main_df=df.withColumn('cleaned_song_name',trans_song_trans(col('song_name')))\
    .withColumn('artist_cleaned',artist_trans(col('artist')))\
    .withColumn('for_lyrics',concat(lit('https://genius.com/'),\
                                    col('artist_cleaned'),lit('-'),col('cleaned_song_name'),lit('-lyrics')))
    lyr=[]
    for i in range(100):
        lyr.append(get_from_genius(main_df.collect()[i][-1]))
    lyrics_dataframe=spark().createDataFrame(lyr,StringType())
    final_df=main_df.join(lyrics_dataframe)
    final_df=final_df.withColumnRenamed('value','lyrics')
    return final_df
def to_csv(df):
    return df.write.csv('spotify_spark.csv')

to_csv(transform_df(create_dataframe()))    
