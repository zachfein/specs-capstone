import requests
from pprint import pprint


def get_teams():
    teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams').json()['teams']

    for teams in teams:
        team_names = teams['teamName']
        team_id = teams['id']


def display_roster():
    roster = requests.get('https://statsapi.web.nhl.com/api/v1/teams/1/roster').json()['roster']

    for player in roster:
        player_name = player['person']['fullName']
        player_position = player['position']['name']
        jersey_number = player['']
        # return player_name
        print(player_name, player_position)
        
display_roster()