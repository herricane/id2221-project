import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import *


class SpotifyClient(object):
    def __init__(self):
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_info(self, track_id):
        track_info = self.sp.track(track_id=track_id)
        track_name = track_info['name']

        artist_id = track_info['artist'][0]['id']
        artist_info = self.sp.artist(artist_id=artist_id)
        artist_name = artist_info['name']

        genres = artist_info['genres']

        return {'name': track_name, 'artist': artist_name, 'genres': genres}
