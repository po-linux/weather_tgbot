from aiogram import types, Dispatcher
import requests
from environs import Env
from tgbot.handlers.coordinates import get_coordinates

env = Env()
env.read_env(".env")


def get_wt_api_path(location):
    lat, lon = get_coordinates(location)
    api_key = env.str("WT_API_KEY")
    api_host = env.str("WT_API_HOST")
    api_params = f"units=metric&lat={lat}&lon={lon}&appid={api_key}"
    api_path = api_host + "?" + api_params
    return api_path


async def get_weather(message: types.Message):
    location = message.text
    api_path = get_wt_api_path(location)
    response = requests.get(api_path)
    wt_json = response.json()
    temp = wt_json["main"]["temp"]
    feels = wt_json["main"]["feels_like"]
    msg = f"Температура в {location} - {temp}°C.\n"
    msg += f"Ощущается как {feels}°C."
    await message.answer(msg)


def register_weather(dp: Dispatcher):
    dp.register_message_handler(get_weather)
    #dp.register_message_handler(get_weather, commands=["weather"], state="*")
