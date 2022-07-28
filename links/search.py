from serpapi import GoogleSearch
import os

API_KEY = os.environ.get('API_KEY')

__all__ = ['get_link']

def request_urls(recipe):
    params = {
        "engine": "google",
        "q": recipe,
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results

def get_link(recipe):
    results = request_urls(recipe)
    if "recipes_results" in results:
        recipe_results = results["recipes_results"][0]['link']
    else:
        google_url = "https://www.google.com/search?q="
        recipe_results = google_url + recipe
        
    return recipe_results

