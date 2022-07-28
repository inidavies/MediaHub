import requests
import os

API_KEY = os.environ.get('RECIPE_API_KEY')
API_HOST = os.environ.get('RECIPE_API_HOST')
URL = "https://tasty.p.rapidapi.com/recipes/list"

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_recipes']

def get_recipes(ingredient):
    """
    Accesses other functions in order to get data from API
    """
    response = request_recipes(ingredient)

    if type(response) is list:
        processed_info = process_json(response)
        return processed_info
    else:
        return -1

def request_recipes(ingredient):
    ''' This should return a dictionary of recipes '''
    # Specifies the query string and the size of the results expected
    querystring = {"from": "0", "size": "30", "q": ingredient}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    response = requests.get(URL, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()['results']
        return data
    else:
        str(r.status_code) + ': ' + str(r.reason)

def process_json(recipe_list):
    """
    Extracts desired data from API response
    """
    data_container = []

    for recipe in recipe_list:
        if "name" in recipe and "thumbnail_url" in recipe and "video_url" in recipe and "description" in recipe:
            if recipe["name"] != None and recipe["thumbnail_url"] != None and recipe["video_url"] != None and recipe["description"] != None:
                print(recipe["description"])
                recipe_name = recipe["name"]
                recipe_video = recipe["video_url"]
                recipe_thumbnail = recipe["thumbnail_url"]
                recipe_descr = recipe["description"]
                current_recipe = {'name': recipe_name,
                                'link': recipe_video,
                                'thumbnail': recipe_thumbnail,
                                'description': recipe_descr}
                data_container.append(current_recipe)
    return data_container

#print(get_recipes("rice"))