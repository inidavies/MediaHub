from flask import Flask, render_template
from flask import url_for, flash, redirect
from flask import session, request
import requests
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
import os
from recipes import get_recipes
from movies import get_movies
from music import get_music
from anime import get_anime
from books import get_books
from db import create_tables
from db import get_table

# Variables to be used globally
Search_Term = ""
Search_Type = ""
Search_Results = []
Saved_Tiles = {"book":[], "music":[], "movie":[], "anime":[], "recipe":[]}

# Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

def search_bar():
    global Search_Term
    global Search_Type
    global Search_Results
    Search_Type = request.form.get('list_type')
    Search_Term = request.form.get('search_bar')
    

    if request.method == 'POST':
        if Search_Type == "all":
            book_results = get_books(Search_Term)
            if book_results == -1:
                book_results = []

            movie_results = get_movies(Search_Term)
            if movie_results == -1:
                movie_results = []

            anime_results = get_anime(Search_Term)
            if anime_results == -1:
                anime_results = []

            music_results = get_music(Search_Term)
            if music_results == -1:
                music_results = []

            recipe_results = get_recipes(Search_Term)
            if recipe_results == -1:
                recipe_results = []

            results_pt1 = book_results + movie_results + anime_results
            results_pt2 = music_results + recipe_results
            Search_Results =  results_pt1 + results_pt2
            if Search_Results == []:
                Search_Results = -1
            return True

        elif Search_Type == "books":
            Search_Results = get_books(Search_Term)

            return True

        elif Search_Type == "movies":
            Search_Results = get_movies(Search_Term)
            return True

        elif Search_Type == "anime":
            Search_Results = get_anime(Search_Term)
            return True

        elif Search_Type == "music":
            Search_Results = get_music(Search_Term)
            return True

        elif Search_Type == "recipes":
            Search_Results = get_recipes(Search_Term)
            return True
        
        else:
            add_tile()


def add_tile():
    # The get the type and the index of the selected tile in the search results
    tile_index = int(request.form.get('tile_content'))
    new_tile = Search_Results[tile_index]
    tile_type = request.form.get("type")
    

    # Gets all the tiles in the chosen type
    saved_types = Saved_Tiles[tile_type]



    # Get all the links in the saved tiles
    saved_links = []
    for tile in saved_types:
        saved_links.append(tile["link"])
    
    # Add if the current link is not in the saved tiles
    if new_tile["link"] not in saved_links:
        Saved_Tiles[tile_type].append(new_tile)
        #Create db tables and retrieve info from item
        create_tables(Saved_Tiles)



# Assign the flask app an secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/intro", methods=['GET', 'POST'])
def intro():
    return render_template('intro.html')

# Home webpage function
@app.route("/", methods=['GET', 'POST'])
def home():
    global Search_Term
    global Search_Type

    # Search bar function
    search = search_bar()
    if search == True:
        return redirect(url_for("results", search=Search_Term))

    return render_template('home.html', results=Search_Results, 
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))


# Inspiration board webpage function
@app.route("/results/<search>", methods=['GET', 'POST'])
def results(search):
    global Search_Term
    global Search_Type
    global Search_Results

    # Search bar function    
    search = search_bar()
    if search == True:
        return redirect(url_for("results", search=Search_Term))
    
    return render_template('results.html', results=Search_Results, 
                           search_term=search, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))


# Displays all saved tiles
@app.route("/all", methods=['GET', 'POST'])
def all():
    display_tiles = []
    for type in Saved_Tiles:
        if Saved_Tiles[type] != []:
            display_tiles.append(get_table(type))
    return render_template('all.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))

# Displays saved book tiles
@app.route("/books", methods=['GET', 'POST'])
def books():
    display_tiles = []
    if Saved_Tiles["book"] != []:
        display_tiles = get_table("book")
    return render_template('books.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))

# Displays saved movie tiles
@app.route("/movies", methods=['GET', 'POST'])
def movies():
    display_tiles = []
    if Saved_Tiles["movie"] != []:
        display_tiles = get_table("movie")
    return render_template('movies.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))

# Displays saved music tiles
@app.route("/music", methods=['GET', 'POST'])
def music():
    display_tiles = []
    if Saved_Tiles["music"] != []:
        display_tiles = get_table("music")
    return render_template('music.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))

# Displays saved anime tiles
@app.route("/anime", methods=['GET', 'POST'])
def anime():
    display_tiles = []
    if Saved_Tiles["anime"] != []:
        display_tiles = get_table("anime")
    return render_template('anime.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))

# Displays saved recipes tiles
@app.route("/recipes", methods=['GET', 'POST'])
def recipes():
    display_tiles = []
    if Saved_Tiles["recipe"] != []:
        display_tiles = get_table("recipe")
    return render_template('recipes.html', tiles=display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))

# User can manually add things here
@app.route("/favs", methods=['GET', 'POST'])
def edits():
    return render_template('edits.html',
                           search_term=Search_Term, 
                           list_books=url_for("books"),
                           list_all=url_for("all"),
                           list_movies=url_for("movies"),
                           list_music=url_for("music"),
                           list_anime=url_for("anime"),
                           list_recipes=url_for("recipes"))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
