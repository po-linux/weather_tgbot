from aiogram import Dispatcher
from aiogram.types import Message


i = 0


async def user_start(message: Message):
    await message.reply("Hello, user!")


async def user_flip(message: Message):
    answers = [
        "Орёл", "Решка", "Орёл", "Решка",
        "Мне похуй", "Мне тоже",
        "Базаришь?",  "Конечно!"
    ]
    global i
    if i >= len(answers):
        i = 0
    answer = answers[i]
    i += 1
    await message.answer(answer)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_flip, commands=["flip"], state="*")
