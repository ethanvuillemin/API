import hug
import random
import requests
import json

api = hug.get(on_invalid=hug.redirect.not_found)
url_station = 'https://www.juleshaag.fr/devIA/devAPI/station_information.json'

@hug.get('/hello')
def hello():
    return 'Hello, world!'

@hug.get('/val')
def val():
    return random.randint(0, 100)

@api.urls('/val2', examples='nb=1')
def generate_random_values(nb: hug.types.number):
    values = [random.randint(-1000, 1000) for _ in range(nb)]
    data = {"values": values}
    return data

@api.urls('/calc/add', examples='number_1=1&number_2=2')
def add(number_1: hug.types.number, number_2: hug.types.number):
    return number_1 + number_2

@api.urls('/calc/prod', examples='number_1=1&number_2=2')
def prod(number_1: hug.types.number, number_2: hug.types.number):
    return number_1 * number_2

@api.urls('/img', examples='num=1')
def img(num: hug.types.number):
    return hug.redirect.to(f'https://www.juleshaag.fr/devIA/devAPI/{num}.png')

@api.urls('/station_velo', examples='id=1')
def station_velo(id: hug.types.number):
    data=requests.get(url_station).json()
    for content in data['data']['stations']:
            if id == int(content['station_id']):
                return content
    return {"error": "Station vélo non trouvée"}

@api.urls('/station_velo2', examples='id=30&addr')
def station_velo(id: hug.types.number, addr: hug.types.text =''):
    data = requests.get(url_station).json()
    for content in data['data']['stations']:
        if id == int(content['station_id']):
            if addr == '':
                return content
            elif addr == 'address':
                return content['address']
            else:
                return {"error": "Mauvais paramètre pour 'addr', veuillez utiliser : 'address'"}
    return {"error": "Station vélo non trouvée"}

if __name__ == '__main__':
    hug.API(__name__).http.serve()