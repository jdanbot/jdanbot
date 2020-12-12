from .token import bot
from .wiki import getWiki
from .lurk import lurk


@bot.message_handler(commands=["speedlurk"])
def speedlurk(message):
    lurk(message, True)


@bot.message_handler(commands=["speedwiki"])
def speedwiki(message):
    getWiki(message, "ru", True)


@bot.message_handler(commands=["speedtest"])
def speedtest(message):
    getWiki(message, "ru", True)
    lurk(message, True)
