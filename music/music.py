from ytmusicapi import YTMusic
# import Flask

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_music']


def music(song_search):
    ytmusic = YTMusic()
    search_results = ytmusic.search(song_search , "songs")
    return search_results

def request_music(song_search):
    data_container=[]
    base_url = "https://www.youtube.com/watch?v="
    music_data = music(song_search)
    #print(music_data[0]["thumbnails"])
    for song in music_data:
        songName = song['title']
        mainArtist = song['artists'][0]['name']
        videoLink = base_url + str(song['videoId'])
        image = song['thumbnails'][1]['url']
        current_song = {"search": song_search, "name": songName, "artist": mainArtist, "link": videoLink, "thumbnail": image}
        data_container.append(current_song)
        
    return data_container

def get_music(song_search):
    response = request_music(song_search)
    if type(response) == list and response != []:
        return response
    else:
        return -1

# print(get_music("Sia"))
