import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials

ClientID =  "3f20832558d44a45ba41ce63fbd2d6df"
ClientSecret = "d7b6be227b324d5cbc4e76edcb324ab2"

link1 = "https://open.spotify.com/album/4u8vi1mU7J7STOQ3qCfoJQ?highlight=spotify:track:7HkHQtCrhVmOkjJySAcUhD"
link2 = "https://open.spotify.com/album/6gkwOLmk0ALMOjWs5WhAEr?highlight=spotify:track:6brl7bwOHmGFkNw3MBqssT"
link3 = "https://open.spotify.com/album/4uiCnolZv9pf1BREEozzZ3?highlight=spotify:track:4haXaGmb5jURAhk9HmgLwz"


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=ClientID,
                                                           client_secret=ClientSecret))

# results = sp.search(q='weezer', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])

trackid = link3.split("track:", 1)[1]
track1 = sp.track(trackid)
artistid = track1['artists'][0]['id']
artist1 = sp.artist(artistid)
albumid = track1['album']['id']
album1 = sp.album(albumid)

track1_name = track1['name']
artist1_name = artist1['name']
artist1_genre = artist1['genres']
album1_genre = album1['genres']
print(track1_name)
print(artist1_name)
print(artist1_genre)
#print(album1_genre)


API_key = "75e0124f06c470a954205f180725a583"
Shared_secret = "6aec2ee1ab0f9c379ca53c8ce73c9e94"
username = "gigalomaniacs"

#url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=AINSEL&api_key=75e0124f06c470a954205f180725a583&format=json"
url1 = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={}&artist={}&track={}&format=json"
url_r = url1.format(API_key,artist1_name,track1_name)
response = requests.get(url_r).json()

track1_tags = response['track']['toptags']
print(track1_tags)