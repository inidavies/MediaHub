from ytmusicapi import YTMusic
# import Flask

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_music']


def music(name):
    ytmusic = YTMusic()
    search_results = ytmusic.search(name , "songs")
    return search_results

def request_music(name):
    data_container=[]
    base_url = "https://www.youtube.com/watch?v="
    music_data = music(name)
    for song in music_data:
        songName = song['title']
        mainArtist = song['artists'][0]['name']
        videoLink = base_url + str(song['videoId'])
        current_song = {"name": songName, "artist": mainArtist, "link": videoLink}
        data_container.append(current_song)
        
    return data_container

def get_music(name):
    response = request_music(name)
    if type(response) == list and response != []:
        return response
    else:
        return -1

#print(get_music("O1223342"))
