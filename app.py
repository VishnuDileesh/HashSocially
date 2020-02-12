from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

import os

project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir, "hashsocially.db"))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'myveryverysecretlysecretsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():

    if request.method == 'POST':

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        print(username)
        print(email)
        print(password)


    return render_template('signup.html')

@app.route('/sign-in', methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        print(email)
        print(password)

    return render_template('signin.html')


if __name__ == '__main__':
    app.run()
