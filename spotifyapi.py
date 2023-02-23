import base64
import json
import os
from requests import post, get
from dotenv import load_dotenv


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token() -> str:
    """
    Function, that returns user token from the api.
    """
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url ='https://accounts.spotify.com/api/token'

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def get_auth_header(token: str):
    """
    Function, that returns authorization header.
    """
    return {"Authorization": "Bearer " + token}


def search_for_artist(token: str, artist_name: str) -> dict:
    """
    Function, that returns dict, which indcludes all the information about
    given artist by it's name.
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print('No artist with such name!')
        return None
    return json_result[0]


def get_songs_by_artist(token: str, artist_id: str):
    """
    Function, that returns top-10 artist's songs by his id.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_available_markets(token: str, song_id: str):
    """
    Func
    """
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['available_markets']





token = get_token()
artist = search_for_artist(token, 'Oxxymiron')
print(artist['id'])
print(artist['name'])
# if __name__ == '__main__':
#     token = get_token()
#     print("Type artist's or group name: ")
#     artist_name = input('>>> ')
#     result = search_for_artist(token, artist_name)
#     print(f"You are talking about {result['name']}!\n")
#     if result:
#         artist_id = result["id"]
#         print("You can check top-10 songs of this artist(band) or check the most\
#  popular song (1 - top-10 songs, 2 - most popular)\n")
#         choice = int(input())
#         if choice == 1:
#             songs = get_songs_by_artist(token, artist_id)
#             for ind, sng in enumerate(songs):
#                 print(f"{ind + 1}. {sng['name']}")
#         elif choice == 2:
#             songs = get_songs_by_artist(token, artist_id)
#             for ind, sng in enumerate(songs):
#                 print(sng['name'])
#                 break
#         else:
#             print('Invalid input!')
