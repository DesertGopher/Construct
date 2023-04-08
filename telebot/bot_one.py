import os
import logging
import asyncio
import requests
from datetime import date

from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text


logging.basicConfig(level=logging.INFO)
CONF_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.abspath(CONF_DIR / 'config' / '.env'))
token = os.getenv('bot_token')


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Категории товаров", "Что новенького?"]
    keyboard.add(*buttons)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Что новенького?"))
async def with_puree(message: types.Message):
    result = requests.get('http://127.0.0.1:8005/news/get_last')
    reply = str(
        "Из последних новостей:" + '\n' +
        '<b>' + str(result.json()['title']) + '</b>' + '\n' +
        '<i>' + str(result.json()['news']) + '</i>' + '\n' +
        '<u>' + 'от ' + str(result.json()['pub_date'][:10]) + '</u>'
    )
    await message.reply(str(reply), parse_mode="html")


@dp.message_handler(lambda message: message.text == "Категории товаров")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
