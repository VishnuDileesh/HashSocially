from flask import Flask, request, render_template, redirect

app = Flask(__name__)

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


