"""
This module works with SpotifyAPI and search info about special artist.
"""
import base64
import json
import os
from requests import post, get
from dotenv import load_dotenv
import pycountry


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
    result = post(url, headers=headers, data=data, timeout=10)
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
    assert isinstance(token, str), 'Invalid token!'
    assert isinstance(artist_name, str), 'Invalid artist name!'

    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers, timeout=10)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print('No artist with such name!')
        return None
    return json_result[0]


def get_songs_by_artist(token: str, artist_id: str):
    """
    Function, that returns top-10 artist's songs by his id.
    """
    assert isinstance(token, str), 'Invalid token!'
    assert isinstance(artist_id, str), 'Invalid artist id!'

    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout=10)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_available_markets(token: str, song_id: str):
    """
    Function, that returns availiable markets fro song with help of its id.
    """
    assert isinstance(token, str), 'Invalid token!'
    assert isinstance(song_id, str), 'Invalid song id!'

    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout=10)
    json_result = json.loads(result.content)
    return json_result['available_markets']


if __name__ == '__main__':
    my_token = get_token()
    print("\nType artist's or group name: ")
    artist_name_ = input('>>> ')
    artist = search_for_artist(my_token, artist_name_)
    print(f"You are talking about {artist['name']}!\n")
    if artist:
        artist_id_ = artist["id"]
        print("You can check top-10 songs of this artist(band) or check the most\
 popular song (1 - top-10 songs, 2 - most popular)\n")
        choice = int(input('>>> '))
        if choice == 1:
            songs = get_songs_by_artist(my_token, artist_id_)
            for ind, sng in enumerate(songs):
                print(f"{ind + 1}. {sng['name']}\n")
        elif choice == 2:
            songs = get_songs_by_artist(my_token, artist_id_)
            for ind, sng in enumerate(songs):
                curr_song = sng['id']
                print(f"Most popular song: {sng['name']}\n")
                break
            print('You can check available markets(countries), where you can listen to this song!\
 Do you wanna check it out? (1 - yes, 2 - no)\n')
            choice = input(">>> ")
            if choice == '1':
                for i in get_available_markets(my_token, curr_song):
                    if pycountry.countries.get(alpha_2=i):
                        print(pycountry.countries.get(alpha_2=i).name)
        else:
            print('Invalid input!')
