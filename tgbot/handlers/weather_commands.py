from aiogram import types, Dispatcher

import tgbot.handlers.weather as wt
from tgbot.keyboards import inline
from tgbot.handlers.coordinates import get_location


# Commands
async def cmd_temperature(message: types.Message):
    location = get_location()
    msg = wt.get_temperature(location)
    await message.answer(msg, reply_markup=inline.TEMPERATURE)


async def cmd_wind(message: types.Message):
    location = get_location()
    msg = wt.get_wind(location)
    await message.answer(msg, reply_markup=inline.WIND)


async def cmd_suntime(message: types.Message):
    location = get_location()
    msg = wt.get_suntime(location)
    await message.answer(msg, reply_markup=inline.SUNTIME)


# Callbaks
async def call_temperature(callback: types.CallbackQuery):
    location = get_location()
    msg = wt.get_temperature(location)
    await callback.message.answer(msg, reply_markup=inline.TEMPERATURE)


async def call_wind(callback: types.CallbackQuery):
    location = get_location()
    msg = wt.get_wind(location)
    await callback.message.answer(msg, reply_markup=inline.WIND)


async def call_suntime(callback: types.CallbackQuery):
    location = get_location()
    msg = wt.get_suntime(location)
    await callback.message.answer(msg, reply_markup=inline.SUNTIME)


def register_weather(dp: Dispatcher):
    dp.register_message_handler(cmd_temperature, commands=["temperature"], state="*")
    dp.register_message_handler(cmd_wind, commands=["wind"], state="*")
    dp.register_message_handler(cmd_suntime, commands=["suntime"], state="*")

    dp.register_callback_query_handler(call_temperature, text="temperature")
    dp.register_callback_query_handler(call_wind, text="wind")
    dp.register_callback_query_handler(call_suntime, text="suntime")
