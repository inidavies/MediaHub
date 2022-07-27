from flask import Flask, render_template
from flask import url_for, flash, redirect
from flask import session, request
import requests
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
import os
from recipes import get_recipes

# Variables to be used globally

# Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

# Assign the flask app an secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route("/intro", methods=['GET', 'POST'])
def intro():
    return render_template('intro.html')

# Home webpage function
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        type = request.form.get('type')
        print(type)
        if type == "all":
            redirect(url_for("results"))
    return render_template('home.html', list_all=url_for("lists"))


# Inspiration board webpage function
@app.route("/results", methods=['GET', 'POST'])
def results():
    return render_template('results.html')


# Author credit webpage function
@app.route("/lists", methods=['GET', 'POST'])
def lists():
    return render_template('lists.html')


@app.route("/favs", methods=['GET', 'POST'])
def edits():
    return render_template('edits.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
