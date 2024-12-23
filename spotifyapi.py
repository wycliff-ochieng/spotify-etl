import requests
from datetime import datetime,timedelta
import json
import datetime
import os
import urllib.parse
from dotenv import load_dotenv
import base64
from requests import post,get

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

code = 'AQBkL1XsxSNFMs4_izc4u_dM6xTwIiNt7V6V6-NdxdPeFCAIz6BF_kwm17swxmuqjvLymzG90aG3aB46a6z4tnDkRQEV1i_Q228hjIk8R0Mmy2YsrK_elAU3NNflF588h1nvx03ZZpqKd-FSQ-8j9P490EgKMk9OKWZv8t8CJKkHSll1FdeKbD9Ur25DgG0LIBc-FFNp2QvQUaDhPrQEkukN9yttPw'
USER_ID = 'wyckie ochieng'
ACCESS_TOKEN = 'BQCxHq5C0XAN1lph-Hm527ioTZirojDlgGS1y5DBRXszzjvedeL11TyMUE8Wu-NbI8nh5GgnSe7XFXr95i9RnroPo8F2brz1jOIb3mlsk8cQoomqUrAk1z_VZ4N-82_3jLZPu5yLRMIQhWq91YFA79JS-kuTX1XevtaT8uDHyUoo1L9RmfUOa9Niu4MLcwqSzKiQqKolOeFXzDEfuKE'
def get_data():

    headers = {
        'Accept':'Application/json',
        'Content-Type':'Application/json',
        'Authorization':'Bearer {token}'.format(token=ACCESS_TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = (yesterday.timestamp()) * 1000

    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(time=yesterday_unix_timestamp),headers=headers)

    data = r.json()
    return data

data = get_data()
print(data)


def get_authorization_url(client_id):
    url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": "2a97936b0ae54f31939ed2d51862ddef",
        "response_type": "code",
        "redirect_uri": "https://developer.spotify.com/dashboard",  # Replace with your redirect URI
        "scope": "user-read-recently-played"  # Add the required scope here
    }
    return f"{url}?{urllib.parse.urlencode(params)}"

print("Go to this URL to authorize:")
print(get_authorization_url("client_id"))


def get_user_token(client_id, client_secret, code):
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://developer.spotify.com/dashboard"  # Must match the redirect URI above
    }
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()  # Access token and refresh token
    else:
        print(f"Error fetching token: {response.status_code}, {response.text}")
        return None

def get_recently_played_songs(token):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

import requests
import base64

def refresh_access_token(refresh_token, client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        json_result = response.json()
        if "access_token" in json_result:
            return json_result["access_token"]
        else:
            print("Unexpected response format:", json_result)
    else:
        print("Error refreshing token:", response.status_code, response.text)
    return None

# Replace with your actual values

refresh_token = "AQA7m5OSYaPNodS7LFskygZUP1cAv4Ci5wBZANmpC1ezsTAjVdLaAxqEy2kDAqSPP7UFgLwOs3JEjaEPPMVnnv1_YmhMyd9qXUpUFQDocfFEHsXng-j8Cc4snpu8YMq-TbU"

new_access_token = refresh_access_token(refresh_token, client_id, client_secret)
if new_access_token:
    print("New Access Token:", new_access_token)
else:
    print("Failed to refresh access token.")

# Example Usage:
#client_id = "your_client_id_here"
#client_secret = "your_client_secret_here"
#code = "your_authorization_code_here"

token_data = get_user_token(client_id, client_secret, code)
print(token_data)
if token_data:
    access_token = token_data['access_token']
    recent_songs = get_recently_played_songs(access_token)
    print(recent_songs)


    