import requests
import json
import time
from model import *

class PlayersData:
    def __init__(self, data):
        self.data = data
        self.session = session
    
    def add_data(self, **elements):
        self.session.add(self.data(**elements))
        return self.session.commit()
    
def extract_players_data():
    page_number = 0
    while True:
        page_number += 1
        query = {'page': str(page_number - 1), 'per_page': '25'}

        try:
            response_API = requests.get('https://www.balldontlie.io/api/v1/players', timeout=50, params=query)
            response_API.raise_for_status()
            
        except requests.exceptions.RequestException as err:
                print(err)
                time.sleep(20)

        try:
            playersData = json.loads(response_API.text)
            
            if not playersData['data']:
                break

        except json.JSONDecodeError as err:
            print(err)
        
        
        for item in playersData['data']:
            player_id = item['id']
            existing_player = session.query(Player).filter_by(id=player_id).first()
            if existing_player:
                continue
            if item['height_inches'] == None:
                item['height_inches'] = ''
            if item['height_feet'] == None:
                item['height_feet'] = ''
            PlayersData(Player).add_data(
                id=item['id'], 
                first_name=item['first_name'], 
                last_name=item['last_name'], 
                height_inches=item['height_inches'], 
                height_feet=item['height_feet'],
                )
        