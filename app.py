from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import os, re
import requests
from secrets import *

project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir, "hashsocially.db"))

API_URL = 'https://api.ritekit.com/v1/stats/auto-hashtag?post='

API_OPTIONS = '&maxHashtags=5&hashtagPosition=auto&client_id='

app = Flask(__name__)

app.config['SECRET_KEY'] = 'myveryverysecretlysecretsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'sign_in'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))


class PostHash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash_text = db.Column(db.String(100))
    hash_tags = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():

    if request.method == 'POST':

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('sign_up'))

        hashed_password = generate_password_hash(password, method='sha256')


        new_user = User(username=username, email=email, password=hashed_password)


        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('sign_in'))


    return render_template('signup.html')

@app.route('/sign-in', methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('sign_in'))

        login_user(user)

        return redirect(url_for('dashboard'))


    return render_template('signin.html')


@app.route('/sign-out')
@login_required
def sign_out():
    logout_user()

    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')



@app.route('/post-text', methods=["POST"])
@login_required
def post_text():

    if request.method == "POST":

        post_text = request.form["post_text"]

        print(post_text)

       
        post_url = API_URL + post_text + API_OPTIONS + CLIENT_ID

        print(post_url)

        r = requests.get(post_url)

        data = r.json()

        
        data_tags = data['post']


        tags = re.compile(r"#(\w+)")

        hashtags = tags.findall(data_tags)

        print(hashtags)

        new_hash_post = HashPost(hash_text=post_text,hash_tags=hashtags, created_by=current_user.id)

        db.session.add(new_hash_post)
        db.session.commit()



        return redirect(url_for('dashboard'))









if __name__ == '__main__':
    app.run()
