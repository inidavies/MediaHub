import requests
import os
import re
from pprint import pprint

RECIPE_API_KEY = os.environ.get('RECIPE_API_KEY')
RECIPE_API_HOST = os.environ.get('RECIPE_API_HOST')

URL = "https://tasty.p.rapidapi.com/recipes/list"

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_recipes']

def get_recipes(ingredient):
    """
    Accesses other functions in order to get data from API
    """
    response = request_recipes(ingredient)

    if type(response) is list:
        processed_info = process_json(response, ingredient)
        return processed_info
    else:
        return -1

def request_recipes(ingredient):
    ''' This should return a dictionary of recipes '''
    # Specifies the query string and the size of the results expected
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q":ingredient, "imageSize":"THUMBNAIL"}

    headers = {
        "X-RapidAPI-Key": RECIPE_API_KEY,
        "X-RapidAPI-Host": RECIPE_API_HOST
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()['hits']
        return data
    else:
        return str(response.status_code) + ': ' + str(response.reason)

def process_json(recipe_list, ingredient):
    """
    Extracts desired data from API response
    """
    data_container = []

    for item in recipe_list:
        recipe = item["recipe"]
        if "label" in recipe and "image" in recipe and "shareAs" in recipe:
            if recipe["label"] != None and recipe["image"] != None and "shareAs" != None:
                recipe_name = recipe["label"]
                recipe_thumbnail = recipe["image"]
                recipe_video = recipe["shareAs"]
                current_recipe = {"search":ingredient, 'dish':recipe_name,
                                'link': recipe_video,
                                'thumbnail': recipe_thumbnail}
                data_container.append(current_recipe)

    if data_container == []:
        data_container = -1
    return data_container

#print(get_recipes("rice"))