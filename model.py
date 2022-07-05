from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from os import environ

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=True, nullable=False)
    last_name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
    
    def __repr__(self):
        return f"""<User user_id={self.user_id}
                   email={self.email} 
                   first_name={self.first_name} 
                   last_name={self.last_name}
                   password={self.password}>"""

class Team(db.Model):
    __tablename__ = "teams"

    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    team_name = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    public = db.Column(db.Boolean)

    def __init__(self, team_name, user_id, public):
        self.team_name = team_name
        self.user_id = user_id
        self.public = public

    def __repr__(self):
        return f"""<Team team_id={self.team_id}
                   team_name={self.team_name}
                   user_id={self.user_id}
                   public={self.public}>"""


class Rostered_Players(db.Model):
    __tablename__ = "rostered_players"

    rostered_player_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"))
    player_id = db.Column(db.Integer, unique=True)

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['POSTGRES_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)