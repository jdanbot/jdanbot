from aiogram import Dispatcher
from .config import settings

from aiogram import Bot

bot = Bot(token=settings.tokens.bot_token)
dp = Dispatcher(bot)
