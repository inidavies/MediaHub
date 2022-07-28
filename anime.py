import kitsupy
def anime():
    animeName = input("What anime do you want: ")
    results = list(kitsupy.search('anime', animeName).values())
    resultsKeys = list(kitsupy.search('anime', animeName).keys())
    position = results.index(animeName)
    animeID = resultsKeys[position]
    rating = kitsupy.get_info('anime', animeID)['averageRating']
    episodeCount = kitsupy.get_info('anime', animeID)['episodeCount']
    trailer = "https://www.youtube.com/watch?v=" + kitsupy.get_info('anime', animeID)['youtubeVideoId']
    image = kitsupy.get_info('anime', animeID)['posterImage']['original']

    return animeName, rating, episodeCount, trailer, image



print(anime())
