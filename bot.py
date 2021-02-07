import traceback

from bot import *
from bot.bot import bot, dp
from aiogram import executor


try:
    executor.start_polling(dp)

except Exception:
    bot.send_message("795449748",
                     f"`{str(traceback.format_exc())}`",
                     parse_mode="Markdown")
