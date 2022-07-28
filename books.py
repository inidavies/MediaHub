import requests
import json
import os
import pandas as pd
import sqlalchemy as db
import urllib.request
from pprint import pprint

#book_apikey = os.environ.get('BOOK_APIKEY')
search = input("Please enter a book title ?")
#defining a function to access the api and send a get request
def find_books():
        url = f'https://www.googleapis.com/books/v1/volumes?q={"search"}&key=AIzaSyD_3CEF5P_6azVom7nW_Hs-ECYrXSAbm_M'
        #send request to API
        response = requests.get(url)
        #parse json into python as dictionary 
        book_data = response.json()

        book_info = book_data["items"][0]["volumeInfo"]
        author = book_info["authors"]

        print(f"\nTitle: {book_info['title']}")
        print(f"Author: {author}")
        #print(f"\nBuyLink: {book_info['buyLink']}")
        #print(f"\ncoverPhoto: {book_info['thumbnail']}")

        #print(data['items']['volumeInfo']['title'])

       

find_books()                    