import email
from flask import (Flask, render_template, request, redirect, flash, session, url_for)
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined, Template
from views import get_teams, display_roster
from pprint import pprint
from model import *
from wtform_fields import *
from os import environ

app = Flask(__name__)

app.config["SECRET_KEY"] = environ["SECRET_KEY"]
db = SQLAlchemy(app)

app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/teams')
def rosters():
    return render_template("teams.html", teams=get_teams()) 

@app.route('/nhl-team-roster/<id>')
def nhl_roster(id):
    return render_template("nhlteam.html", roster=display_roster(id))

@app.route('/roster')
def teams():
    return render_template("roster.html")

@app.route('/register', methods = ["GET", "POST"])
def register():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        first_name = reg_form.first_name.data
        last_name = reg_form.last_name.data
        email = reg_form.email.data
        password = reg_form.password.data

        user_object = User.query.filter_by(email=email).first()
        if user_object:
            return 'Email is already in use. Please try another email.'

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')

    return render_template('register.html', form=reg_form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logmein', methods = ['GET', 'POST'])
def logmein():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if not user:
        return('User not found')

    login_user(user)

    return 'You are now logged in'

@app.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")

if __name__ == '__main__':

    connect_to_db(app)

    app.run(debug=True, host="0.0.0.0")