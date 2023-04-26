import requests
import json
from datetime import datetime, timedelta
import time

#Gets yesterdays date 
yesterday_datetime = datetime.now() - timedelta(days=1)
yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')

file = open('%s.txt' % yesterday_date, 'w')
page_number = 0
while True:
    page_number += 1
    query = {'page': str(page_number), 'per_page': '25', 'dates': str(yesterday_date)}

    try:
        response_API = requests.get('https://www.balldontlie.io/api/v1/stats', timeout=50, params=query)
        if response_API != 200:
            time.sleep(20)
        response_API.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    #Reads API and opens json:
    playersData = json.loads(response_API.text)
    #Data about players:
    allPlayers = len(playersData['data'])
    complete_data = ''

    for player in range(0, allPlayers):
        item = playersData['data'][player]
        if item['player']['first_name'] != None:
            complete_data += str(item['player']['first_name'])
        complete_data += ','
        if item['player']['last_name'] != None:
            complete_data += str(item['player']['last_name'])
        complete_data += ','
        if item['pts'] != None:
            complete_data += str(item['pts'])      
        complete_data += ','
        if item['reb'] != None:
            complete_data += str(item['reb'])
        complete_data += ','
        if item['stl'] != None:
            complete_data += str(item['stl'])
        complete_data += '\n'
        file.write(complete_data)
    if complete_data is not True:
        break
file.close()