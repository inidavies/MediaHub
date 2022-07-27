from ytmusicapi import YTMusic
import Flask


ytmusic = YTMusic()

search_results = ytmusic.search("Suge" , "songs")
print("https://www.youtube.com/embed/" + str(search_results[0]['videoId']))