from aiogram import types, Dispatcher
import requests
from environs import Env

env = Env()
env.read_env(".env")


def get_coords():
    lat, lon = 55.75, 37.62
    return lat, lon


def get_api_path():
    lat, lon = get_coords()
    api_key = env.str("WT_API_KEY")
    api_host = env.str("WT_API_HOST")
    api_params = f"units=metric&lat={lat}&lon={lon}&appid={api_key}"
    api_path = api_host + "?" + api_params
    return api_path


async def get_weather(message: types.Message):
    api_path = get_api_path()
    response = requests.get(api_path)
    wt_json = response.json()
    city = wt_json["name"]
    temp = wt_json["main"]["temp"]
    feels = wt_json["main"]["feels_like"]
    msg = f"Температура в {city} равна {temp}°C.\n"
    msg += f"Ощущается как {feels}°C."
    await message.answer(msg)


def register_weather(dp: Dispatcher):
    dp.register_message_handler(get_weather, commands=["weather"], state="*")
