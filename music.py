from ytmusicapi import YTMusic
# import Flask


def music():
    song = input(" what song would you like?: ")
    ytmusic = YTMusic()
    search_results = ytmusic.search(song , "songs")
    songName = search_results[0]['title']
    mainArtist = search_results[0]['artists'][0]['name']
    videoLink = "https://www.youtube.com/watch?v=" + str(search_results[0]['videoId'])
    thumbnail = search_results[0]['thumbnails'][0]['url']

    return songName, mainArtist, videoLink, thumbnail

print(music())