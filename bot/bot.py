# -- coding: utf8 --

import traceback

from components import *
from components.token import bot


try:
    bot.polling()

except:
    bot.send_message("795449748",
                     f"`{str(traceback.format_exc())}`",
                     parse_mode="Markdown")
