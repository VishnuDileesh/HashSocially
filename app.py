from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/sign-up')
def sign_up():

    return render_template('signup.html')

@app.route('/sign-in')
def sign_in():

    return render_template('signin.html')


