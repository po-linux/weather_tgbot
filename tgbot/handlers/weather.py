import requests
from environs import Env
from enum import IntEnum
from datetime import datetime

from tgbot.handlers.location import get_coordinates


env = Env()
env.read_env(".env")

class WindDirection(IntEnum):
    North = 0
    Northeast = 45
    East = 90
    Southeast = 135
    South = 180
    Southwest = 225
    West = 270
    Northwest = 315


def get_wt_api_url(location):
    coordinates = get_coordinates(location)
    if not coordinates:
        return False

    api_host = env.str("WT_API_HOST")
    api_key = env.str("WT_API_KEY")
    lon, lat = coordinates.split(' ')
    api_params = f"units=metric&lat={lat}&lon={lon}&appid={api_key}"

    api_url = api_host + "?" + api_params
    return api_url


def get_wind_direction(degrees):
    degrees = round(degrees / 45) * 45
    if degrees == 360:
        degrees = 0
    return WindDirection(degrees).name


def get_temperature(location):
    api_url = get_wt_api_url(location)
    if not api_url:
        return "Неизвестное местоположение, введите заново"

    response = requests.get(api_url)
    wt_json = response.json()

    temp = wt_json["main"]["temp"]
    feels = wt_json["main"]["feels_like"]

    msg = f"Температура на данный момент составляет {temp}°C.\n"
    msg += f"Ощущается как {feels}°C."
    return msg


def get_wind(location):
    api_url = get_wt_api_url(location)
    if not api_url:
        return "Неизвестное местоположение, введите заново"

    response = requests.get(api_url)
    wt_json = response.json()

    direction = get_wind_direction(wt_json["wind"]["deg"])
    speed = wt_json["wind"]["speed"]

    msg = f"Напрвлелие ветра - {direction}, cкорость {speed} м/с."
    return msg


def get_suntime(location):
    api_url = get_wt_api_url(location)
    if not api_url:
        return "Неизвестное местоположение, введите заново"

    response = requests.get(api_url)
    wt_json = response.json()

    sunrise_ts = datetime.fromtimestamp(wt_json["sys"]["sunrise"])
    sunset_ts = datetime.fromtimestamp(wt_json["sys"]["sunset"])
    sunrise = sunrise_ts.strftime("%H:%M")
    sunset = sunset_ts.strftime("%H:%M")

    msg = f"Восход солнца - {sunrise}, закат солнца - {sunset}."
    return msg