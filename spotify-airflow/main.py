from dotenv import load_dotenv
import os
from requests import post,get
import base64
import json
import urllib.parse
import requests


load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scopes = os.getenv('SCOPES')
print(client_id,client_secret)

def get_auth_url():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scopes
    }
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return url

auth_url = get_auth_url()
print("Go to the following URL in your browser and log in:\n", auth_url)
#webbrowser.open(auth_url)
code = input("Enter code:")

def get_token(code):
    auth_string=client_id + ":" + client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes),"utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers={"Authorization":"Basic "+auth_base64,
             "Content-Type":"application/x-www-form-urlencoded"}
    data={"grant_type":"authorization_code",
          "code":code,
          "redirect_uri":redirect_uri}
    result=post(url,headers=headers,data=data)
    result_json=json.loads(result.content)
    token=result_json["access_token"]
    return token

token=get_token(code)


def get_recently_played_tracks(token, limit=10):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "limit": limit
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)

    for item in data['items']:
        track = item['track']
        print(f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")


get_recently_played_tracks(token)


