import requests
import json
import pandas as pd
import sqlalchemy as db

#  Dataframe
col_names = ['Title', 'Release Date', 'Trailer']
df = pd.DataFrame(columns=col_names)

def movie_search(movie_input):
        i = 0
        youtube = 'https://www.youtube.com/watch?v='
        request = requests.get('https://api.themoviedb.org/3/search/movie?api_key=ca247a677e49a57329443e35dfc24974&language=en-US&page=1&query={}&include_adult=false'.format(movie_input)).json()
        try:
            #  To get the movie titles
            while i < len(request['results']):
                vid_request = requests.get('https://api.themoviedb.org/3/movie/{}/videos?active_nav_item=Trailers&api_key=ca247a677e49a57329443e35dfc24974&language=en-US'.format(request['results'][i]['id'])).json()
                movie_id = request['results'][i]['original_title']
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
                    df.loc[len(df.index)] = [request['results'][i]['original_title'], request['results'][i]['release_date'], youtube + key]
                else:
                    no_key = 'No trailer for this movie'
                    df.loc[len(df.index)] = [request['results'][i]['original_title'], request['results'][i]['release_date'], no_key]
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