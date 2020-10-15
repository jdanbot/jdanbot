from .token import bot
from .lib.prettyword import prettyword
from random import choice, randint


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
    number = randint(0, 200)

    if number == 0:
        bot.reply_to(message, "Иди нахуй))")

    else:
        nedeli = number / 7
        date = choice(["дней", "месяцев"])

        if date == "дней":
            true_date = prettyword(number, ["день", "дня", "дней"])

        elif date == "месяцев":
            true_date = prettyword(number, ["месяц", "месяца", "месяцев"])

        if number % 7 == 0:
            bot.reply_to(message, f'{name} уйдет через {int(nedeli)} {prettyword(int(nedeli), ["неделя", "недели", "недель"])}')
        else:
            print(number % 7)
            bot.reply_to(message, f'{name} уйдет через {int(nedeli)} {prettyword(int(nedeli), ["неделя", "недели", "недель"])} и {int(number % 7)} {prettyword(int(number % 7), ["день", "дня", "дней"])}')


@bot.message_handler(commands=["da_net"])
def da_net(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_message(message.chat.id, choice(["Да", "Нет"]), reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, choice(["Да", "Нет"]))
