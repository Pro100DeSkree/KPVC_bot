import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from os import path
import os


base_dir = path.dirname(path.abspath(__file__))

# Якщо запущено на Heroku, то взяти токен з PATH ОС. Якщо ні, то з файлу конфігу
if base_dir in "/app":
    TOKEN = os.environ.get('TOKEN')
else:
    import config
    TOKEN = config.TOKEN
loop = asyncio.get_event_loop()  # Для створення потоку
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, loop=loop, storage=storage)
