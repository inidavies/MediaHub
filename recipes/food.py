import requests
import os
import re
from pprint import pprint

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
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q":ingredient, "imageSize":"THUMBNAIL"}

    headers = {
        "X-RapidAPI-Key": "2f0847bcc5mshe005ab687e03bf2p1f34dejsn709aedc05a6a",
        "X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()['hits']
        return data
    else:
        return str(response.status_code) + ': ' + str(response.reason)

def process_json(recipe_list):
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
                current_recipe = {'dish': recipe_name,
                                'link': recipe_video,
                                'thumbnail': recipe_thumbnail}
                data_container.append(current_recipe)
    return data_container

#pprint(request_recipes("rice"))
#pprint(get_recipes("rice"))
'''
import requests
from pprint import pprint

url = "https://edamam-recipe-search.p.rapidapi.com/search"

querystring = {"q":"chicken", "imageSize":"SMALL"}

headers = {
	"X-RapidAPI-Key": "2f0847bcc5mshe005ab687e03bf2p1f34dejsn709aedc05a6a",
	"X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

pprint(response.json()["hits"][0])
'''

'''from py_edamam import Edamam
from pprint import pprint
e = Edamam(recipes_appid='62dfd4d9',
           recipes_appkey='097906ea45712e4232a85c3b80df858c')

recipes_list = e.search_recipe("onion and chicken")

# keys scrapped from web demo, but you can provide yours above
nutrient_data = e.search_nutrient("1 large apple")

foods_list = e.search_food("chocolate")
pprint(recipes_list["hits"][5]["recipe"]["image"])

'''
