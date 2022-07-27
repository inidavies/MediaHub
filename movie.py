import requests
import json
import pandas as pd
import sqlalchemy as db
import urllib.request
import re

col_names = ['Title', 'Release Date', 'Trailer']
df = pd.DataFrame(columns=col_names)

def movie_search(movie_input):
        i = 0
        request = requests.get('https://api.themoviedb.org/3/search/movie?api_key=ca247a677e49a57329443e35dfc24974&language=en-US&page=1&query={}&include_adult=false'.format(movie_input)).json()
        movie_input = movie_input.replace(' ', '+')
        html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + movie_input)
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        try:
            while i < len(request['results']):
                html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + request['results'][i]['original_title'])
                video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
                movie_id = request['results'][i]['original_title']
                df.loc[len(df.index)] = [request['results'][i]['original_title'], request['results'][i]['release_date'], 'https://www.youtube.com/watch?v=' + video_ids[0]]
                i += 1
        except IndexError:
            print('No movies for this search')


def main():
    movie_input = str(input('Search for movie or "no" to exit when prompted: '))
    while movie_input != ('no' or 'No'):
        movie_search(movie_input)
        print('Search for another movie?')
        movie_input = str(input())
    for i in range(len(df)):
        print(df.loc[i, :].to_string())
if __name__ == '__main__':
    main()