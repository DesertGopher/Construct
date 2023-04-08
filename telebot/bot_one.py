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

_NP_PHOTO_PATH = os.path.abspath(CONF_DIR / 'construct' / 'media')


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Категории товаров", "Что новенького?"]
    keyboard.add(*buttons)
    await message.answer("Приветствуем в лучшем в мире боте для ВКР по вебу. Чем могу быть полезен?",
                         reply_markup=keyboard)


@dp.message_handler(Text(equals="Что новенького?"))
async def whats_new(message: types.Message):
    result = requests.get('http://127.0.0.1:8005/news/get_last')
    reply = str(
        "Из последних новостей:" + '\n' +
        '<b>' + str(result.json()['title']) + '</b>' + '\n' +
        '<i>' + str(result.json()['news']) + '</i>' + '\n' +
        '<u>' + 'от ' + str(result.json()['pub_date'][:10]) + '</u>'
    )
    pic = open((str(_NP_PHOTO_PATH) + '/' + str(result.json()['picture'])).replace('\\', '/'), 'rb')
    await bot.send_photo(message.from_user.id, photo=pic, caption=str(reply),
                         reply_to_message_id=message.message_id, parse_mode='html')


@dp.message_handler(Text(equals="Категории товаров"))
async def whats_new(message: types.Message):
    result = requests.get('http://127.0.0.1:8005/categories/get-list')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    reply = str('Вот что мы имеем...' + '\n')
    for i in result.json():
        buttons.append(i['name'])
        reply += ' - <i>' + str(i['name']) + '</i>\n'
    keyboard.add(*buttons)
    reply += "Какая категория Вас интересует?"
    await message.answer(reply, reply_markup=keyboard, parse_mode='html')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
