import telebot
import os
import json

if "TOKEN" in os.environ:
    bot = telebot.TeleBot(os.environ["TOKEN"])
    heroku = True

else:
    with open("../token.json") as token:
        heroku = False
        bot = telebot.TeleBot(json.loads(token.read())["token"])
