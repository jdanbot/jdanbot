from .token import bot
from .lib.fixHTML import fixHTML
import json
import yaml


@bot.message_handler(commands=["message"])
def msg(message):
    if message.chat.id == 795449748:
        try:
            params = message.text.split(maxsplit=2)
            bot.send_message(params[1], params[2])
        except Exception as e:
            bot.reply_to(message, f"`{e}`", parse_mode="Markdown")


@bot.message_handler(content_types=['document', 'video'],
                     func=lambda message: message.chat.id == -1001189395000)
def delete_w10(message):
    try:
        if message.video.file_size == 842295 or \
           message.video.file_size == 912607:
            bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


@bot.message_handler(content_types=['sticker'],
                     func=lambda message: message.chat.id == -1001176998310 or \
                                          message.chat.id == -1001374137898)
def delete_misha(message):
    try:
        if message.sticker.file_size == 20340 and \
           not message.sticker.is_animated and \
           message.from_user.id == 1248462292:
            bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


@bot.message_handler(commands=["detect"])
def detect_boicot(message):
    if message.text.find("бойкот") != -1:
        bot.reply_to(message, "Вы запостили информацию о бойкоте, если вы бойкотировали, то к вам приедут с паяльником")
    else:
        bot.reply_to(message, "Бойкот не обнаружен")


@bot.message_handler(commands=["sticker_id"])
def get_sticker_id(message):
    try:
        bot.reply_to(message, message.reply_to_message.sticker.file_id)

    except:
        bot.reply_to(message, "Ответь на сообщение со стикером")


@bot.message_handler(commands=["delete"])
def delete(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        if message.reply_to_message.from_user.id == "1121412322":
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    except:
        pass


@bot.message_handler(commands=["list"])
def commandslist(message):
    bot.reply_to(message, "/w, /van, /potatowiki, /speedlurk, /speedwiki, /speedtest, /wget")


@bot.message_handler(["to_yaml"])
def toyaml(message):
    if message.reply_to_message:
        code = message.reply_to_message.text
        try:
            j = json.loads(code)
            y = yaml.dump(j, allow_unicode=True)[:4096]
            bot.reply_to(message,
                         f"<code>{fixHTML(y)}</code>",
                         parse_mode="HTML")
        except:
            bot.reply_to(message, "Произошла ошибка при перекодировании")
    else:
        bot.reply_to(message, "Ответь на json")
        return


@bot.message_handler(["if"])
def if_(message):
    options = message.text.split()

    if len(options) < 3:
        bot.reply_to(message, "Напиши аргументы :/")

    else:
        result = options[1] == options[2]
        t = "<code>"     # open code tag
        tc = "</code>"   # close code tag

        bot.reply_to(message,
                     f"{t}{options[1]} == {options[2]}{tc}: <b>{result}</b>",
                     parse_mode="HTML")


@bot.message_handler(commands=["to_json"])
def to_json(message):
    try:
        bot.send_message(message.chat.id,
                         message.reply_to_message.text.replace("'", "\"")
                                                      .replace("False", "false")
                                                      .replace("True", "true")
                                                      .replace("None", '"none"')
                                                      .replace("<", '"<')
                                                      .replace(">", '>"'))
    except:
        bot.reply_to(message, "Ответь на сообщение с python-кодом, который надо превравить в json")
