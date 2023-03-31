import os
import logging

from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

CONF_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.abspath(CONF_DIR / 'config' / '.env'))
token = os.getenv('bot_token')

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
