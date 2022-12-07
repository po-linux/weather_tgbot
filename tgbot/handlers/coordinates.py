# from aiogram import types, Dispatcher
import requests
from environs import Env

from aiogram import types, Dispatcher
from tgbot.keyboards import inline

env = Env()
env.read_env(".env")

location = "Москва"


def get_crd_api_url(location):
    api_key = env.str("GEO_API_KEY")
    api_host = env.str("GEO_API_HOST")
    api_params = f"apikey={api_key}&format=json&geocode={location}"
    # https://geocode-maps.yandex.ru/1.x/?apikey=ваш API-ключ&format=json&geocode=Тверская+6 - порядок параметров не важен
    api_url = api_host + "?" + api_params
    return api_url


def get_coordinates(location):
    api_url = get_crd_api_url(location)
    response = requests.get(api_url)
    crd_json = response.json()
    try:
        geobj = crd_json["response"]["GeoObjectCollection"]["featureMember"][0]
        coordinates = geobj["GeoObject"]["Point"]["pos"]
    except:
        coordinates = False
    return coordinates


# эта функция нужна, чтобы из других модулей получить значение location
def get_location():
    global location
    return location


# чтобы установить новые значения для переменной location
async def set_location(message: types.Message):
    global location
    location = message.text
    msg = f"Установлена новая локация: {location}"
    await message.answer(msg, reply_markup=inline.WEATHER)


def register_location(dp: Dispatcher):
    dp.register_message_handler(set_location, content_types=types.ContentTypes.TEXT, state="*")
