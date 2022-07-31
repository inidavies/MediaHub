import kitsupy

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_anime']


def get_anime(animeName):
    response = process_anime(animeName)
    if type(response) == list and response != []:
        return response
    else:
        return -1

def request_anime(animeName):
    results = kitsupy.search('anime', animeName)
    return  results

def process_anime(animeName):
    base_url = "https://www.youtube.com/watch?v="
    results = request_anime(animeName)
    results.pop('count')
    data_container = []
    for anime in results:
        animeID = anime
        anime_info = get_info(animeID)
        if type(anime_info) is list:
            trailer = base_url + anime_info[0]
            name = results[anime]
            rating = anime_info[1]
            episodeCount = anime_info[2]
            image = anime_info[3]
            current_anime = {"search": animeName, "name": name, "rating": rating,
                            "episodes": episodeCount, "link": trailer,
                            "thumbnail": image}
            data_container.append(current_anime)

    return data_container

def get_info(animeID):
    results = kitsupy.get_info('anime', animeID)
    trailer = results['youtubeVideoId']
    rating = results['averageRating']
    episodeCount = results['episodeCount']
    image = results['posterImage']['original']
    if isinstance(trailer, str):
        return [trailer, rating, episodeCount, image]
    else:
        return -1