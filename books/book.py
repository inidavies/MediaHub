import requests
import json
import os
import pandas as pd
import sqlalchemy as db
import urllib.request
from pprint import pprint

BOOK_API_KEY = os.environ.get('BOOK_API_KEY')

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_books']

#book_apikey = os.environ.get('BOOK_APIKEY')
#defining a function to access the api and send a get request
def find_books(search):
        base_url = "https://www.googleapis.com/books/v1/volumes?q=" 
        url = base_url + search + "&key=" + BOOK_API_KEY
        #send request to API
        response = requests.get(url)
        if response.status_code == 200:
                data = response.json()
                if data["totalItems"] != 0:
                        return data
        else:
                str(response.status_code) + ': ' + str(response.reason)

def process_books(book_data, search):
        #parse json into python as dictionary 
        book_info = book_data["items"]
        data_container = []
        current_book = {}
        for book in book_info:
                book_details = book["volumeInfo"]
                if "title" in book_details and "authors" in book_details and "previewLink" in book_details and "imageLinks" in book_details:
                        images = book_details["imageLinks"]
                        if "thumbnail" in images:
                                book_title = book_details["title"]
                                authors = book_details["authors"]

                                book_authors = authors[0]
                                if len(authors) > 1:
                                        for author in authors:
                                                book_authors = ", " + author

                                book_purchase = book_details['previewLink'] 
                                book_coverphoto = images["thumbnail"]
                                current_book = {"name":book_title, "author":book_authors, "link":book_purchase, "thumbnail":book_coverphoto, "search": search}
                
                data_container.append(current_book)

        return data_container

def get_books(search):
        response = find_books(search)
        if type(response) == dict:
                book_list = process_books(response, search)
                return book_list
        else:
                return -1


print(get_books("yes"))