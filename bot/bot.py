# -- coding: utf8 --

import traceback

# import components.stickers
# import components.text
# import components.art
# import components.habr
# import components.youtube
# import components.menu
# import components.status
# import components.wiki
# import components.photo
# import components.random
# import components.rules
# import components.memes
# import components.mrakopedia
# import components.wget
# import components.lurk
# import components.inline
# import components.test
# import components.math
# import components.dev
# import components.crypto
# import components.ban
from components import *
from components.token import bot


try:
    bot.polling()

except:
    bot.send_message("795449748",
                     f"`{str(traceback.format_exc())}`",
                     parse_mode="Markdown")
