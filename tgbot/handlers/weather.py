from aiogram import types, Dispatcher
import json
import requests

api_key = 'f95e776f6f05ffd238e6709cd03db248'
lat, lon = 55.75, 37.62
api_path = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"


async def get_weather(message: types.Message):
    response = requests.get(api_path)
    wt_dict = response.json()
    wt_json = json.dumps(wt_dict)
    await message.answer(wt_json)


def register_weather(dp: Dispatcher):
    dp.register_message_handler(get_weather, commands=["weather"], state="*")

