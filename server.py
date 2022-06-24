from flask import (Flask, render_template, request, redirect, flash, session)
from jinja2 import StrictUndefined
from model import User, db, Team, Rostered_Players, connect_to_db


app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/rosters')
def rosters():
    return render_template("roster.html")

@app.route('/teams')
def teams():
    return render_template("teams.html")

@app.route('/register', methods = ["POST"])
def register_user():
    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]

    user = User(email = email, password = password, first_name = first_name, last_name = last_name)
    db.session.add(user)
    db.session.commit()
    flash("Account created successfully!")
    return render_template("register.html")

@app.route('/login', methods = ["GET", "POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    if User.query.filter_by(email=email):
        query = User.query.filter_by(email = email)
        results = query.first()
        if results.password == password:
            session["email"] = email
            flash("Login successful")
            return render_template("login.html")
        else:
            flash("Incorrect password")
            return render_template("login.html")
    else:
        flash("Incorrect username")
        return render_template("login.html")



if __name__ == '__main__':

    connect_to_db(app)

    app.run(debug=True, host="0.0.0.0")