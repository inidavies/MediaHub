from ytmusicapi import YTMusic
# import Flask


def music():
    ytmusic = YTMusic()
    search_results = ytmusic.search("Suge" , "songs")
    songName = search_results[0]['title']
    mainArtist = search_results[0]['artists'][0]['name']
    videoLink = "https://www.youtube.com/watch?v=" + str(search_results[0]['videoId'])

    return songName, mainArtist, videoLink

music()