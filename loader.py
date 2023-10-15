from aiogram import Bot, Dispatcher
from data import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.postgres import Database
import asyncio


loop = asyncio.get_event_loop()
db = loop.run_until_complete(Database.create())
storage = MemoryStorage()
bot = Bot(token=TOKEN_API, parse_mode = 'HTML')
dp = Dispatcher(bot=bot, storage=storage)
