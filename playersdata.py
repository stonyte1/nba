import requests
import json
import time

file = open('nbaplayers.txt', 'w')
page_number = 0
while True:
    page_number += 1
    query = {'page': str(page_number), 'per_page': '25'}

    try:
        response_API = requests.get('https://www.balldontlie.io/api/v1/players', timeout=50, params=query)
        if response_API != 200:
            time.sleep(20)
        response_API.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.TooManyRedirects:
        print()
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    #Reads API and opens json:
    playersData = json.loads(response_API.text)
    #Data about players:
    file.write('Name,Surname,Height(inches),Height(feet)\n')
    allPlayers = len(playersData['data'])
    complete_data = ''

    for player in range(0, allPlayers):
        item = playersData['data'][player]
        if item['first_name'] is not None:
            complete_data += str(item['first_name'])
        complete_data += ','
        if item['last_name'] is not None:
            complete_data += str(item['last_name'])
        complete_data += ','
        if item['height_inches'] is not None:
            complete_data += str(item['height_inches'])
        complete_data += ','
        if item['height_feet'] is not None:
            complete_data += str(item['height_feet'])
        complete_data += '\n'
        file.write(complete_data)
    if complete_data is not True:
        break
file.close()