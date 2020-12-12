from .token import bot, heroku
from .lib.telegram import Telegram
from .lib.photo import Photo
from random import choice


@bot.message_handler(commands=["resize"])
def resize(message):
    tg = Telegram(bot)

    params = tg.parse(message, 3)

    if params == 404:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `3`",
                     parse_mode="Markdown")
        return

    print(params)

    try:
        photo = tg.photo(message)
    except AttributeError:
        bot.reply_to(message, "Ответьте на фото")
        return

    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")

    try:
        img.resize([int(params[1]), int(params[2])])
    except Exception as e:
        bot.reply_to(message,
                     f"Произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["text"])
def text(message):
    tg = Telegram(bot)

    params = message.text.split(" ", maxsplit=4)

    if len(params) != 5:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `5`",
                     parse_mode="Markdown")
        return

    print(params)

    try:
        photo = tg.photo(message)
    except AttributeError:
        bot.reply_to(message, "Ответьте на фото")
        return

    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")
    try:
        img.font("OpenSans-Bold.ttf" if heroku else "../OpenSans-Bold.ttf", int(params[1]))
        img.text(params[2], img.parseXY(params[3]), params[4])
    except Exception as e:
        bot.reply_to(message,
                     f"Произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["t"])
def t(message):
    tg = Telegram(bot)

    params = message.text.split(" ", maxsplit=1)

    if len(params) == 1:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `2`",
                     parse_mode="Markdown")
        return

    print(params)

    try:
        photo = tg.photo(message)
    except AttributeError:
        bot.reply_to(message, "Ответьте на фото")
        return

    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")
    try:
        img.font("OpenSans-Bold.ttf" if heroku else "../OpenSans-Bold.ttf", 75)
        img.text("black", (50, 50), params[1])
    except Exception as e:
        bot.reply_to(message,
                     f"Произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["rectangle"])
def rectangle(message):
    tg = Telegram(bot)

    params = tg.parse(message, 4)

    if params == 404:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `4`",
                     parse_mode="Markdown")
        return

    print(params)
    photo = tg.photo(message)
    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")

    try:
        img.rectangle(img.parseXY(params[2]), img.parseXY(params[3]), params[1])
    except Exception as e:
        bot.reply_to(message,
                     f"Во время создания фото произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["random_color", "color"])
def random_color(message):
    options = message.text.split(" ", maxsplit=1)
    if len(options) == 1:
        randlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]

        color = ""
        for i in range(0, 6):
            color += str(choice(randlist))

        color = "#" + color

    else:
        if options[1].startswith("#"):
            color = options[1]
        else:
            bot.reply_to(message, "Вводи цвет в формате hex")
            return

    img = Photo()

    try:
        img.rectangle((0, 0), (220, 220), color)
        img.rectangle((0, 159), (220, 220), "#282C34")
        font = "JetBrainsMono-Bold.ttf" if heroku else "../JetBrainsMono-Bold.ttf"
        img.font(font, 47)
        img.text("#DB9D63", (13, 160), color, outline=False)
        img.text("#FFF", (13, 160), "#", outline=False)
    except Exception as e:
        bot.reply_to(message,
                     f"Во время создания фото произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id,
                   img.save(),
                   caption=f"`{color}`",
                   reply_to_message_id=message.message_id,
                   parse_mode="Markdown")
    img.clean()
