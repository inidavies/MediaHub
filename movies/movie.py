import requests
import json
import pandas as pd
import sqlalchemy as db
import os

#  Dataframe
col_names = ['Title', 'Release Date', 'Trailer']
df = pd.DataFrame(columns=col_names)

MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
TITLE_URL_A = "https://api.themoviedb.org/3/search/movie?"
TITLE_URL_B = f'api_key={MOVIE_API_KEY}'
TITLE_URL_C = "&language=en-US&page=1&"

TRAILER_URL_A = "https://api.themoviedb.org/3/"
TRAILER_URL_C = f'api_key={MOVIE_API_KEY}&language=en-US'

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_movies']

def get_movies(movie_input):
        TITLE_URL_D = f"query={movie_input}&include_adult=false"
        data_container = []
        i = 0
        youtube = 'https://www.youtube.com/watch?v='
        data = requests.get(TITLE_URL_A + TITLE_URL_B + TITLE_URL_C + TITLE_URL_D)
        request = data.json()
        try:
            #  To get the movie titles
            while i < len(request['results']):
                current_id = request['results'][i]['id']
                TRAILER_URL_B = f"movie/{current_id}/videos?active_nav_item=Trailers&"
                IMAGE_URL_A = f'https://api.themoviedb.org/3/movie/{current_id}?'
                data = requests.get(TRAILER_URL_A + TRAILER_URL_B + TRAILER_URL_C)
                img = requests.get(IMAGE_URL_A + TRAILER_URL_C)
                img_request = img.json()
                vid_request = data.json()
                movie_id = request['results'][i]['original_title']
                poster = img_request['poster_path']
                poster_url = f'https://image.tmdb.org/t/p/original{poster}'
                j = 0
                key = ''
                #  To get the trailers from each movie
                while j < len(vid_request['results']):
                    movie_video = vid_request['results'][j]['type']
                    if movie_video == 'Trailer':
                        key = vid_request['results'][j]['key']
                        break
                    j += 1
                #  To catch movies without trailers and put into dataframe
                if len(key) >= 1:
                    movie_name = request['results'][i]['original_title']
                    movie_date = request['results'][i]['release_date']
                    movie_link = youtube + key
                    movie_img = poster_url
                    df.loc[len(df.index)] = [movie_name, movie_date, movie_link]
                    current_movie = {"name": movie_name, "date": movie_date, 
                                     "link": movie_link, 'thumbnail': movie_img,
                                     "search":movie_input}
                    data_container.append(current_movie)
                i += 1
        except IndexError:
            return -1

        if data_container == []:
            data_container = -1
        return data_container

# print(get_movies("Yes"))