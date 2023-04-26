import requests
import json
import time

class Players():
    def __init__(self, name, surname, height_inches, height_feet):
        self.name = name
        self.surname = surname
        self.height_inches = height_inches
        self.height_feet = height_feet
    
    def player_data(self):
        return f'{self.name}, {self.surname}, {self.height_inches}, {self.height_feet}\n'

with open('nbaplayers.txt', 'w') as file:
    file.write('Name,Surname,Height(inches),Height(feet)\n')
    
    page_number = 0
    while True:
        page_number += 1
        query = {'page': str(page_number), 'per_page': '25'}

        try:
            response_API = requests.get('https://www.balldontlie.io/api/v1/players', timeout=50, params=query)
            response_API.raise_for_status()
        except requests.exceptions.RequestException as err:
                print(err)
                time.sleep(20)

        try:
            playersData = json.loads(response_API.text)
        except json.JSONDecodeError as err:
            print(err)
            break
        
        for item in playersData['data']:
            if item['height_inches'] == None:
                item['height_inches'] = ''
            if item['height_feet'] == None:
                item['height_feet'] = ''
            players = Players(str(item['first_name']), str(item['last_name']), str(item['height_inches']), str(item['height_feet']))
            file.write(players.player_data())
    
    file.close()