# A FAIRE : Site web, Authentification OAuth2 Javascript, choisir artistes/tracks/genres ou générer de rien

import requests
import json

import os

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

def request_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    params = {
        "grant_type": "client_credentials",  
        "client_id":CLIENT_ID,
        "client_secret":CLIENT_SECRET
    }
    
    res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=params)
    
    data = json.loads(res.text)
    
    return data

def user_genre(time_range: str, limit: int, access_token: str, number_limit: int):
    headers = {"Authorization": f"Bearer {access_token}"}
    
    url = f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}&offset=0"
    
    res = requests.get(url=url, headers=headers)
    
    data = json.loads(res.text)["items"]
    
    genres = []
    
    for genre in range(limit):
        for number in range(len(data[genre]["genres"])):
            if len(genres) != number_limit:
                genres.append(data[genre]["genres"][number])
        
    return genres

def user_artist_track_id(time_range: str, type:str, access_token: str, number: int):
    headers = {"Authorization": f"Bearer {access_token}"}
    
    url = f"https://api.spotify.com/v1/me/top/{type}?time_range={time_range}"
    
    res = requests.get(url=url, headers=headers)
    
    data = json.loads(res.text)["items"]
    
    artists = []
    
    counter = 0
    artists = []

    for artist in data:
        artists.append(artist["id"])
        counter += 1
        if counter == number:
            break
        
    return artists

def account_informations(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    
    url = "https://api.spotify.com/v1/me"
    
    res = requests.get(url=url, headers=headers)
    
    data = json.loads(res.text)
    
    return data

def create_playlist(name: str, description: str, public: bool, user_id: str, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    
    params = {"name": name,
              "description": description,
              "public": public}
    
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    
    res = requests.post(url=url, headers=headers, data=json.dumps(params))
    
    data = json.loads(res.text)
    
    return data

def add_items_playlist(playlist_id: str, tracks_uris: list, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    
    params = {"uris": tracks_uris}
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    
    res = requests.post(url=url, headers=headers, data=json.dumps(params))
    
    data = json.loads(res.text)
    
    return data

def get_recommendations(seed_artists: str, seed_genres: str, seed_tracks: str, market: str, recommendation_limit: int, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    
    url = f"https://api.spotify.com/v1/recommendations?seed_artists={seed_artists}&seed_genres={seed_genres}&seed_tracks={seed_tracks}&market={market}&limit={recommendation_limit}"
    
    res = requests.get(url=url, headers=headers)
    
    data = json.loads(res.text)
    
    return data

def generate_playlist(playlist_name: str, playlist_description: str, playlist_public: bool, user_id: str, access_token: str, recommendation_limit: int):
    market = account_informations(access_token=access_token)["country"]
    
    playlist = create_playlist(name=playlist_name, description=playlist_description, public=playlist_public, user_id=user_id, access_token=access_token)
    
    song_uris = []
    
    for i in range(recommendation_limit):
        best_user_genre = user_genre(time_range="short_term", limit=recommendation_limit, access_token=access_token, number_limit=recommendation_limit)[i]
        user_artist = user_artist_track_id(time_range="short_term", type="artists", access_token=access_token, number=recommendation_limit)[i]
        user_track = user_artist_track_id(time_range="short_term", type="tracks", access_token=access_token, number=recommendation_limit)[i]
        
        recommendations = get_recommendations(seed_artists=user_artist, seed_genres=best_user_genre, seed_tracks=user_track, market=market, recommendation_limit=recommendation_limit, access_token=access_token)["tracks"]
        
        for song in recommendations:
            song_uri = song["uri"]
            
            song_uris.append(song_uri)
            
    add_items_playlist(playlist_id=playlist["id"], tracks_uris=song_uris, access_token=access_token)
    
access_token = "BQCvtZdwqJ_BdGVIQRfZx6Mh9WPQBfaB9Qo4-JO7QioeYNwdBMoVYhin6JtUMvViFGFAVhewzGSxZ5qgCuf0eGsvJGlIFcMTUv0tB3i9pehSPI8QfSq9HtUt-1N6lI4G-qtq069bZ3rWS0x0nmWjyrAAkk4aJpFdRJ-CDY2Haq0afiW7GQi67YY3kPxsYQB9cBDBlwDj65ruoXx8MinMHTXS8ONJFSGNrOKfRZfBqenycd2wHuC8O6-Cv-2OYJSNB7NXGdlANT6k9_UBlMgv2_LO4bBg3nCY0rN9ZPez0fv-79-bslGaF2O1tD-vc6e08Y00iAzljAOVPUk9g5L59rcIn4G6"

name = "test"
description = "test"
public = False

generate_playlist(name, description, public, user_id=account_informations(access_token=access_token)["id"], access_token=access_token, recommendation_limit=10)