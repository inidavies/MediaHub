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

# Variables to be used globally
Search_Term = ""
Search_Type = ""
Search_Results = []

# Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

def search_bar():
    global Search_Term
    global Search_Type
    global Search_Results

    if request.method == 'POST':
        Search_Type = request.form.get('list_type')
        Search_Term = request.form.get('search_bar')
        if Search_Type == "all":
            book_results = get_books(Search_Term)
            movie_results = get_movies(Search_Term)
            anime_results = get_anime(Search_Term)
            music_results = get_music(Search_Term)
            recipe_results = get_recipes(Search_Term)
            results_pt1 = book_results + movie_results + anime_results
            results_pt2 = music_results + recipe_results
            Search_Results =  results_pt1 + results_pt2
        elif Search_Type == "books":
            Search_Results = get_books(Search_Term)
        elif Search_Type == "movies":
            Search_Results = get_movies(Search_Term)
        elif Search_Type == "anime":
            Search_Results = get_anime(Search_Term)
        elif Search_Type == "music":
            Search_Results = get_music(Search_Term)
        elif Search_Type == "recipes":
            Search_Results = get_recipes(Search_Term)
        return True
    

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
        return redirect(url_for("results", type=type, search_term=Search_Term))
    return render_template('home.html', list_all=url_for("lists"))


# Inspiration board webpage function
@app.route("/results/<type>", methods=['GET', 'POST'])
def results(type):
    global Search_Term
    global Search_Type

    # Search bar function
    search = search_bar()
    if search == True:
        return redirect(url_for("results", type=type, search_term=Search_Term))

    return render_template('results.html', results=Search_Results, search_term = Search_Term)


# Author credit webpage function
@app.route("/lists", methods=['GET', 'POST'])
def lists():
    #Seatrch the list

    return render_template('lists.html')


@app.route("/favs", methods=['GET', 'POST'])
def edits():
    return render_template('edits.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
