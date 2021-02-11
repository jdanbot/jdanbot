from aiogram import executor

from bot import *  # noqa
from bot.config import dp

executor.start_polling(dp)
