import os
import logging
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

_NP_PHOTO_PATH = os.path.abspath(CONF_DIR / 'construct' / 'media')


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Покажи категории", "Что новенького?", "Помоги найти товар", "Что ты умеешь?"]
    keyboard.add(*buttons)
    await message.answer("Приветствуем в лучшем в мире боте для ВКР по вебу.\nЧем могу быть полезен?",
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


@dp.message_handler(Text(equals="Покажи категории"))
async def show_categories(message: types.Message):
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


@dp.message_handler()
async def echo_message(msg: types.Message):
    get_category = requests.get(f'http://127.0.0.1:8005/categories/exist/?name={msg.text}')
    get_product = requests.get(f'http://127.0.0.1:8005/products/name-search/?search={msg.text}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    try:
        try:
            if get_category.json()['is_exist']:
                product_id = get_category.json()['id']
                products_list = requests.get(f'http://127.0.0.1:8005/products/category/{product_id}/')
                reply = str('В данной категории есть следующие товары:' + '\n')
                for i in products_list.json():
                    reply += ' - <i>' + str(i['name']) + '</i>\n'
                reply += "<b>Если хотите подробнее ознакомиться с товаром, напишите его название, или часть.</b>"
                await msg.answer(reply, reply_markup=keyboard, parse_mode='html')
        except:
            if get_product.json() and 'detail' not in get_product.json():
                if len(get_product.json()) > 1:
                    reply = str('По запросу было найдены следующие товары:' + '\n')
                    for i in get_product.json():
                        reply += ' - <i>' + str(i['name']) + '</i>\n'
                        buttons.append(i['name'])
                    keyboard.add(*buttons)
                    reply += "<b>Какой из товаров Вас интересует?</b>"
                    await msg.answer(reply, reply_markup=keyboard, parse_mode='html')
                elif len(get_product.json()) == 1:
                    reply_detail = ""
                    i = get_product.json()[0]

                    reply_detail += '<b>' + str(i['name']) + '</b> от ' + str(i['vendor']) + '\n'
                    if i['discount'] > 0:
                        reply_detail += '<s>' + str(i['price']) + '₽</s> → <b>' + \
                                        str(i['price'] * (1 - i['discount']/100)) \
                                        + '₽</b>\n'
                    else:
                        reply_detail += '<b>' + str(i['price']) + '₽</b>\n'
                    reply_detail += '<i>' + str(i['about']) + '</i>\n'
                    pic = open((str(_NP_PHOTO_PATH) + '/' + str(i['prod_pic'])).replace('\\', '/'), 'rb')
                    await bot.send_photo(msg.from_user.id, photo=pic, caption=str(reply_detail), parse_mode='html')
            else:
                raise Exception
    except:
        buttons = ["/start", "/info"]
        keyboard.add(*buttons)
        text = "Я не могу ничего найти по вашему запросу или не понимаю команды. \n " \
               "Чтобы начать общение введите команду <i>/start</i> или <i>/info</i> " \
               "для информации о моем алгоритме работы"
        await bot.send_message(msg.from_user.id, text, reply_markup=keyboard, parse_mode='html')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
