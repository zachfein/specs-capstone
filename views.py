import requests
from pprint import pprint

def get_teams():
    teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()['teams']
    return teams

def display_roster(id):
    roster = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{id}/roster').json()['roster']
    return roster

def get_player(player_id):
    player = requests.get(f'https://statsapi.web.nhl.com/api/v1/people/{player_id}').json()['people'][0]['fullName']
    return player