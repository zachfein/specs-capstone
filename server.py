from xml.dom import ValidationErr
from flask import (Flask, render_template, request, redirect, flash, session, url_for)
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined, Template
from views import get_teams, display_roster, get_player
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
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/teams')
def rosters():
    return render_template("teams.html", teams=get_teams()) 

@app.route('/nhl-team-roster/<id>')
def nhl_roster(id):
    return render_template("nhlteam.html", roster=display_roster(id))

@app.route('/roster/<team_id>')
def teams(team_id):
    team_name = Team.query.get(team_id).team_name

    players_list = Rostered_Players.query.filter_by(team_id=team_id).all()

    for player in players_list:
        player_name = get_player(player.player_id)

        player.name = player_name

    return render_template("roster.html", players_list=players_list, team_name=team_name)

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
        return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return render_template('home.html')

    return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/addplayer')
def addPlayer():
    player_id = request.args.get('playerid')

    rostered_player = Rostered_Players(team_id=1, player_id=player_id)
    db.session.add(rostered_player)
    db.session.commit()
    
    return render_template('teams.html', teams=get_teams())

def invalid_credentials(form, field):
    email = form.email.data
    password = field.data

    user_object = User.query.filter_by(email=email).first()
    if user_object is None:
        raise ValidationErr('Email or password is incorrect')
    elif password != user_object.password:
        raise ValidationErr('Email or password is incorrect')

if __name__ == '__main__':

    connect_to_db(app)

    app.run(debug=True, host="0.0.0.0")