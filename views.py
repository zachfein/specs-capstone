import requests
from pprint import pprint

def get_teams():
    teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()['teams']
    return teams

def display_roster(id):
    roster = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{id}/roster').json()['roster']
    return roster

