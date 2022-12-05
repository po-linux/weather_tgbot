import requests
from environs import Env
from aiogram import types, Dispatcher
from tgbot.handlers.coordinates import get_coordinates

env = Env()
env.read_env(".env")


def get_wt_api_url(location):
    coordinates = get_coordinates(location)
    if not coordinates:
        return False

    lon, lat = coordinates.split(' ')
    api_key = env.str("WT_API_KEY")
    api_host = env.str("WT_API_HOST")
    api_params = f"units=metric&lat={lat}&lon={lon}&appid={api_key}"
    api_url = api_host + "?" + api_params
    return api_url


async def get_weather(message: types.Message):
    location = message.text
    api_url = get_wt_api_url(location)
    if not api_url:
        await message.answer("Неизвестное местоположение, введите заново")

    response = requests.get(api_url)
    wt_json = response.json()
    temp = wt_json["main"]["temp"]
    feels = wt_json["main"]["feels_like"]
    msg = f"Температура в городе {location} на данный момент составляет {temp}°C.\n"
    msg += f"Ощущается как {feels}°C."
    await message.answer(msg)


def register_weather(dp: Dispatcher):
    dp.register_message_handler(get_weather)
