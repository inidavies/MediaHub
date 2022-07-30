from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
from ytmusicapi import YTMusic
import random


def music(song):
    ytmusic = YTMusic()
    search_results = ytmusic.search(song , "songs")
    songName = search_results[0]['title']
    mainArtist = search_results[0]['artists'][0]['name']
    videoLink = "https://www.youtube.com/watch?v=" + str(search_results[0]['videoId'])
    thumbnail = search_results[0]['thumbnails'][0]['url']

    return songName, mainArtist, videoLink, thumbnail

def randomMusic():
    rand = random.randint(0, 49)
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    pl_id = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'

    listOfTopHits = []

    response = sp.playlist_items(pl_id)
    for i in range(len(response['items'])):
        listOfTopHits.append(response['items'][i]['track']['name'])
    print(music(listOfTopHits[rand]))
    
randomMusic()