# from aiogram import types, Dispatcher
import requests
from environs import Env

from aiogram import types, Dispatcher
from tgbot.keyboards import inline
from tgbot.states.location import Location
from aiogram.dispatcher.storage import FSMContext


env = Env()
env.read_env(".env")


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
'''
 эта функция нужна, чтобы из других модулей получить значение location
def get_location():
    global location
    return location
'''


async def get_location(state: FSMContext):
    data = state.get_data()
    location = data.get('ans')
    await location


# чтобы установить новые значения для переменной location
async def set_location(message: types.Message):
    await message.answer('Укажите новую локацию')
    await Location.location.set()
'''
   global location
    location = message.text
    msg = f"Установлена новая локация: {location}"
    await message.answer(msg, reply_markup=inline.WEATHER)
'''


async def answer_location(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(ans=answer)
    await message.answer(f"Новое местоположение: {answer}", reply_markup=inline.WEATHER)


def register_location(dp: Dispatcher):
    dp.register_message_handler(set_location, commands=["set_location"], state="*")
    dp.register_message_handler(answer_location, content_types=types.ContentTypes.TEXT, state=Location.location)