import requests
import json
import time
from functions.model import *

class GamesData:
    def __init__(self, data):
        self.data = data
        self.session = session   

    def add_data(self, **elements):
        self.session.add(self.data(**elements))
        return self.session.commit()

def extract_games_data():
    page_number = 0
    while True:
        page_number += 1
        query = {'page': str(page_number - 1), 'per_page': '25', 'seasons[]': 2022}

        try:
            response_API = requests.get('https://www.balldontlie.io/api/v1/stats', timeout=50, params=query)
            response_API.raise_for_status()

        except requests.exceptions.RequestException as err:
            print(err)
            time.sleep(20)

        try:
            gamesData = json.loads(response_API.text)

            if not gamesData['data']:
                break

        except json.JSONDecodeError as err:
            print(err)

        for item in gamesData['data']:
            if item['pts'] is None:
                item['pts'] = ''
            if item['reb'] is None:
                item['reb'] = ''
            if item['stl'] is None:
                item['stl'] = ''  
            GamesData(Game).add_data(
                player_id=item['player']['id'], 
                pts=item['pts'], 
                reb=item['reb'], 
                stl=item['stl'], 
                date=item['game']['date'], 
                team=item['team']['name'],
                game_id = item['game']['id'],
                ) 
            