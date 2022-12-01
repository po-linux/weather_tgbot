from aiogram import types, Dispatcher
from random import randrange


async def bot_flip(message: types.Message):
    rand = randrange(2)
    msg = "Yes" if rand else "No"
    """
    0 = False, 1 = True
    msg = ""
    if rand:
        msg = "Yes"
    else:
        msg = "No"
    """
    await message.answer(msg)


def register_flip(dp: Dispatcher):
    dp.register_message_handler(bot_flip, commands=["flip"], state="*")
