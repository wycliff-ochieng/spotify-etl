import requests
from datetime import datetime,timedelta
import json
import datetime
import os
import pandas as pd
import urllib.parse
from dotenv import load_dotenv
import base64
import sqlite3
from requests import post,get
from transform import check_if_data_is_valid
import sqlalchemy
from sqlalchemy import create_engine

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

DATABASE_LOCATION = "sqlite:///most_recents.sqlite"

code = 'AQBZAm0Pgo8ti8e5KqEPmE46seG3FLXo5alJQuWTkk9Djhh-_trjjLk1RdkhwweWJgp2gKgnNMCauLSQDLY7siC1q_Z0XeH6Rp0gPjJ25MRc89hOMpY0U28kJ7w-r6Zr98GkaxkSlKS1lCSzuEQ2obO5Igekwb-aZPROjSOl2nvlR8dATp8HMO8_ICpg7BYO5vC0JRpi11y-0K-rkCiCzchNmUnM6g'

USER_ID = 'wyckie ochieng'

ACCESS_TOKEN = 'BQC306150ZOKykTNfx5rWPQli_zjZkZ73oLXt62gLar_CjunwqHqlBfDBOQcQlR8fA9DkMfg0JQlCxBAqzNS2w13dgiw4LAn0beI0YVPC00PQsYgwuwWIVsrpPq093R9GAWmVI4QAJp7J4wUdqPwhF6zHlRNXhGL02uyEdSOuBb9OfqR5kIIzEi9t5z6JpIYNYy83uo4qDf7v0OdqIQ'

if __name__=="__main__":

    headers = {
        'Accept':'Application/json',
        'Content-Type':'Application/json',
        'Authorization':'Bearer {token}'.format(token=ACCESS_TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(time=yesterday_unix_timestamp),headers=headers)

    data = r.json()
    #print(data)

    song_id = []
    songs_names = []
    artist_names = []
    played_at = []
    timestamps = []

    for song in data["items"]:
        song_id.append(song["track"]["id"])
        songs_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    songs_dict = {
        "song_id" : song_id,
        "songs_names" : songs_names,
        "artist_names" : artist_names,
        "played_at" : played_at,
        "timestamps" : timestamps
    }

    song_df = pd.DataFrame(songs_dict,columns=["song_id","songs_names","artist_names","played_at","timestamps"])
    print(song_df)

    check_if_data_is_valid(song_df)

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect("my_songs.sqlite")
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS most_recents(
        song_id TEXT,
        songs_names VARCHAR(30),
        artist_names VARCHAR(30),
        played_at VARCHAR(50),
        timestamps TIMESTAMP
    )
    """

    cursor.execute(sql_query)
    try:
        song_df.to_sql("most_recents",engine,index="False",if_exists="append")
    except:
        print("Data already exists in the storage system")

    conn.close()
    print("Data laoded and database successfully closed")

