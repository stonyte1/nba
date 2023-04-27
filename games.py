import requests
import json
from datetime import datetime, timedelta
import time

class Games():
    def __init__(self, name, surname, pts, reb, stl):
        self.name = name
        self.surname = surname
        self.pts = pts
        self.reb = reb
        self.stl = stl

    def games_data(self):
        return f'{self.name}, {self.surname}, {self.pts}, {self.reb}, {self.stl}\n'

yesterday_datetime = datetime.now() - timedelta(days=1)
yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')

page_number = 0
while True:
    with open('%s.txt' % yesterday_date, 'a') as file:
        page_number += 1
        query = {'page': str(page_number), 'per_page': '25', 'dates': str(yesterday_date)}

        try:
            response_API = requests.get('https://www.balldontlie.io/api/v1/stats', timeout=50, params=query)
            response_API.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(err)
            time.sleep(20)

        try:
            gamesData = json.loads(response_API.text)
        except json.JSONDecodeError as err:
            print(err)
            file.close()
            break
        
        for item in gamesData['data']:
            if item['pts'] is None:
                item['pts'] = ''
            if item['reb'] is None:
                item['reb'] = ''
            if item['stl'] is None:
                item['stl'] = ''  
            games = Games(item['player']['first_name'], item['player']['last_name'], item['pts'], item['reb'], item['stl']) 
            file.write(games.games_data())

file.close()