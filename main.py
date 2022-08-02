from flask import Flask, render_template
from flask import url_for, flash, redirect
from flask import session, request
import requests
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
import os
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user
from flask_login import login_required, logout_user, current_user
from recipes import get_recipes
from movies import get_movies
from music import get_music
from anime import get_anime
from books import get_books
from datab import create_tables
from datab import get_table
from datab import create_database


# Variables to be used globally
Search_Term = ""
Search_Type = ""
Search_Results = []
Saved_Tiles = {"book":[], "music":[], "movie":[], "anime":[], "recipe":[]}

# Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

def search_bar(user):
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
            add_tile(user)


def add_tile(user):
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
        create_tables(user, Saved_Tiles)


# Make database for flask form
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

db.create_all()
db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



# Assign the flask app an secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/")
@app.route("/intro", methods=['GET', 'POST'])
def intro():
    return render_template('intro.html')

# Home webpage function
@app.route("/home/<user>", methods=['GET', 'POST'])
def home(user):
    global Search_Term
    global Search_Type

    # Search bar function
    search = search_bar(user)
    if search == True:
        return redirect(url_for("results", user=user,
                        search=Search_Term))

    return render_template('home.html', username=user, 
                           results=Search_Results, 
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user), 
                           home = url_for("home", user=user))

# print(Search_Results)
# Inspiration board webpage function 
@app.route("/results/<user>/<search>", methods=['GET', 'POST'])
def results(user, search):
    global Search_Term
    global Search_Type
    global Search_Results

    # Search bar function    
    search = search_bar(user)
    if search == True:
        return redirect(url_for("results", user=user,
                        search=Search_Term))

    return render_template('results.html', results=Search_Results, 
                           search_term=search, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user), 
                           home = url_for("home", user=user))


# Displays all saved tiles
@app.route("/all/<user>", methods=['GET', 'POST'])
def all(user):
    display_tiles = []
    for type in Saved_Tiles:
        display_tiles.append(get_table(user, type))

    return render_template('all.html', tiles=display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user),
                           home = url_for("home", user=user))


# Displays saved book tiles
@app.route("/books/<user>/", methods=['GET', 'POST'])
def books(user):
    display_tiles = []
    display_tiles = get_table(user,"book")
    return render_template('books.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user),
                           home = url_for("home", user=user))


# Displays saved movie tiles
@app.route("/movies/<user>/", methods=['GET', 'POST'])
def movies(user):
    display_tiles = []
    display_tiles = get_table(user,"movie")
    return render_template('movies.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user),
                           home = url_for("home", user=user))


# Displays saved music tiles , home = url_for("home")
@app.route("/music/<user>/", methods=['GET', 'POST'])
def music(user):
    display_tiles = []
    display_tiles = get_table(user,"music")
    return render_template('music.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user), 
                           home = url_for("home", user=user))


# Displays saved anime tiles
@app.route("/anime/<user>/", methods=['GET', 'POST'])
def anime(user):
    display_tiles = []
    display_tiles = get_table(user,"anime")
    return render_template('anime.html', tiles= display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user),
                           home = url_for("home", user=user))


# Displays saved recipes tiles
@app.route("/recipes/<user>/", methods=['GET', 'POST'])
def recipes(user):
    display_tiles = []
    display_tiles = get_table(user,"recipe")
    return render_template('recipes.html', tiles=display_tiles,
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user),
                           home = url_for("home", user=user))

# User can manually add things here
@app.route("/edits/<user>/", methods=['GET', 'POST'])
def edits(user):
    return render_template('edits.html',
                           search_term=Search_Term, 
                           list_books=url_for("books", user=user),
                           list_all=url_for("all", user=user),
                           list_movies=url_for("movies", user=user),
                           list_music=url_for("music", user=user),
                           list_anime=url_for("anime", user=user),
                           list_recipes=url_for("recipes", user=user),
                           home = url_for("home", user=user))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home', user=user))

        return render_template('login.html', form=form, display="block")
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>' 

    return render_template('login.html', form=form, display="none", signup=url_for("signup"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        create_database(new_user.username)
        return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form, login=url_for("login"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
