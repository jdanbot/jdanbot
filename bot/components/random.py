from .token import bot
from .lib.prettyword import prettyword
from .lib.telegram import Telegram
from random import choice, randint


tg = Telegram(bot)


@bot.message_handler(commands=["random_ban", "random"])
def random(message):
    bot.reply_to(message, f"Лови бан на {randint(1, 100)} минут")


@bot.message_handler(commands=["random_putin"])
def random_putin(message):
    random_person(message, choice(["Обнуленец", "Путин", "Путен"]))


@bot.message_handler(commands=["random_lukash", "luk", "lukash"])
def random_lukash(message):
    random_person(message, choice(["Лукашенко", "Лукашеску", "3%", "Саша", "Саня"]))


def random_person(message, name):
    number = randint(0, 500)

    if number == 1:
        bot.reply_to(message, "Иди нахуй))")

    else:
        weeks = number / 7

        if number % 7 == 0:
            bot.reply_to(message, f'{name} уйдет через {int(weeks)} {prettyword(int(weeks), ["неделя", "недели", "недель"])}')
        else:
            bot.reply_to(message, f'{name} уйдет через {int(weeks)} {prettyword(int(weeks), ["неделя", "недели", "недель"])} и {int(number % 7)} {prettyword(int(number % 7), ["день", "дня", "дней"])}')


@bot.message_handler(commands=["da_net"])
def da_net(message):
    tg.delete_message(message)
    bot.reply_to(message, choice(["Да", "Нет"]))
