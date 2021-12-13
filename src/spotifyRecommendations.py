import os
import pandas as pd
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
API_CLIENT_ID = os.getenv('API_CLIENT_ID')
API_CLIENT_SECRET = os.getenv('API_CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(client_id=API_CLIENT_ID, client_secret=API_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def getRecomendations(data):
    my_top10_artists = data.groupby(['artist'])['play_count'].sum().sort_values(ascending=False).head(10).index.tolist()

    top_tracks = pd.DataFrame()
    for artist in my_top10_artists:
        result = sp.search(q='artist:'+artist, type='artist')
        artist_id = result['artists']['items'][0]['id']
        artist_genres = ", ".join(result['artists']['items'][0]['genres'])
        artist_top_tracks = sp.artist_top_tracks(artist_id=artist_id, country='US')
        for track in artist_top_tracks['tracks']:
            track_dict = {}
            track_dict['name'] = track['name']
            track_dict['artist'] = ", ".join([artist['name'] for artist in track['artists']]) 
            track_dict['album'] = track['album']['name']
            track_dict['album_img_url'] = track['album']['images'][0]['url']
            track_dict['genre'] = artist_genres
            track_dict['total_time'] = track['duration_ms']
            track_dict['album_type'] = track['album']['album_type']
            track_dict['preview_url'] = track['preview_url']
            top_tracks = top_tracks.append(track_dict, ignore_index=True)
    
    recommendation = top_tracks.sample(frac=0.1)
    recommendation_list = recommendation.to_dict('records')
    
    return recommendation_list
