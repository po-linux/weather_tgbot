# from aiogram import types, Dispatcher
import requests
from environs import Env


env = Env()
env.read_env(".env")


def get_crd_api_path(location):
    api_key = env.str("GEO_API_KEY")
    api_host = env.str("GEO_API_HOST")
    api_params = f"apikey={api_key}&format=json&geocode={location}"
    api_path = api_host + "?" + api_params
    return api_path


def get_coordinates(location):
    api_path = get_crd_api_path(location)
    response = requests.get(api_path)
    crd_json = response.json()
    geobj = crd_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lon, lat = geobj["Point"]["pos"].split(' ')
    return lat, lon

# https://geocode-maps.yandex.ru/1.x/?apikey=ваш API-ключ&format=json&geocode=Тверская+6 - порядок параметров не важен
