import requests
from datetime import datetime,timedelta
import json
import datetime
import os
import pandas as pd
import urllib.parse
from dotenv import load_dotenv
import base64
from requests import post,get
from transform import check_if_data_is_valid

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

code = 'AQBZAm0Pgo8ti8e5KqEPmE46seG3FLXo5alJQuWTkk9Djhh-_trjjLk1RdkhwweWJgp2gKgnNMCauLSQDLY7siC1q_Z0XeH6Rp0gPjJ25MRc89hOMpY0U28kJ7w-r6Zr98GkaxkSlKS1lCSzuEQ2obO5Igekwb-aZPROjSOl2nvlR8dATp8HMO8_ICpg7BYO5vC0JRpi11y-0K-rkCiCzchNmUnM6g'

USER_ID = 'wyckie ochieng'

ACCESS_TOKEN = 'BQDE6ygqn35O-icPDs4mY5rZODM1JXeHKTa4nQ3RBYfwcRQns9os4W9zD3RvuiiIvyEa0Fg27noZhGi4JI1qCh1WKXY2B0n8YPs2oYP68q0iLkwZ9o0VZh_M9kTnM4P7eava8nrcraTC8_UNTzCycLSxxaNWjkiGZ-pa0ka1Abm2v1qwU8QwxiFCmswgtTtq_-VnVD5cvcrThu2vCSQ'

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

