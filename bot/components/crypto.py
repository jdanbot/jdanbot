from .token import bot
from random import choice
import hashlib


@bot.message_handler(commands=["sha256"])
def sha256(message):
    try:
        if message.reply_to_message.text:
            bot.reply_to(message, hashlib.sha256(bytearray(message.reply_to_message.text.encode("utf-8"))).hexdigest())
        elif message.reply_to_message.document:
            file_id = message.reply_to_message.document.file_id

            document = bot.get_file(file_id)
            bot.reply_to(message, hashlib.sha256(bytearray(bot.download_file(document.file_path))).hexdigest())
        else:
            bot.reply_to(message, hashlib.sha256(bytearray(message.reply_to_message.text.encode("utf-8"))).hexdigest())
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=["generate_password"])
def password(message):
    if len(message.text.split(maxsplit=1)) == 1:
        bot.reply_to(message, "Укажите количество символов в пароле")
        return

    try:
        crypto_type = int(message.text.split(maxsplit=1)[1])
    except:
        bot.reply_to(message, "Введите число")
        return

    if crypto_type > 4096:
        bot.reply_to(message,
                     "Телеграм поддерживает сообщения длиной не больше `4096` символов",
                     parse_mode="Markdown")
        return

    elif crypto_type < 6:
        bot.reply_to(message,
                     "Пароли меньше `6` символов запрещены",
                     parse_mode="Markdown")
        return

    data = []
    password = ""
    # data.extend(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"))
    # data.extend(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper()))
    data.extend(list("abcdefghijklmnopqrstuvwxyz"))
    data.extend(list("abcdefghijklmnopqrstuvwxyz".upper()))
    data.extend(list('~!@#$%^&*()_+-=`[]\\{}|;\':"<>,./?'))
    data.extend(list("0123456789"))

    for num in range(0, crypto_type):
        password += choice(data)

    bot.reply_to(message, password)
