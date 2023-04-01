import os
import logging
import asyncio
import requests

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
    buttons = ["Показать товар", "Без пюрешки"]
    keyboard.add(*buttons)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Показать товар"))
async def with_puree(message: types.Message):
    result = requests.get('http://127.0.0.1:8005/products/10/')
    await message.reply(str(result.json()['id']))


@dp.message_handler(lambda message: message.text == "Без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
