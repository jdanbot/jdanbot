from .token import bot
from .lib.fixHTML import fixHTML
import pyscp
import re

scp = pyscp.wikidot.Wiki('http://scpfoundation.net')


@bot.message_handler(["scp"])
def detectscp(message):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        bot.reply_to(message, "Напиши название scp")
        return

    print(f"[SCP RU] {options[1]}")

    try:
        p = scp(options[1])
        p.title

    except:
        try:
            p = scp("scp-" + options[1])
            p.title
        except:
            bot.reply_to(message, "Не удалось найти scp")
            return

    text = p.text

    # text = re.sub(r"рейтинг: ", "", p.text)

    text = fixHTML(text)
    text = re.sub(r"(\n\n\n|\n\n)", "\n", text)
    text = text.split("\n")

    images = p.images

    try:
        for number, string in enumerate(text):
            if string.find("рейтинг:") != -1:
                del(text[number])

        for number, string in enumerate(text):
            if string.startswith("Дополнение"):
                del(text[number])

            if string.find("Особые условия содержания:") != -1:
                del(text[number])

        for number, string in enumerate(text):
            test = ["Объект №:", "Класс объекта:", "Примеры объектов:", "Описание:"]
            for k in test:
                if string.find(k) != -1:
                    o = string.split(":")[0]
                    print(f"{o = }")
                    text[number] = text[number].replace(o, "<b>" + o + "</b>")

            if "Описание:" in string:
                u = number + 1
            else:
                u = 6

        for number, string in enumerate(text):
            if string.startswith("Дополнение"):
                del(text[number])

        if text[0] == "":
            del(text[0])

        if len(images) != 0:
            del(text[0])

        text = "\n".join(text[:u])

    except Exception as e:
        print(e)
        text = "\n".join(text)

    title = fixHTML(p.title.replace('\n', ''))
    msg = f"<b>{title}</b>\n{text}"[:4096]
    msg = msg.replace("</b>\n\n<b>", "</b>\n<b>")
    # print(msg)

    if len(images) != 0:
        try:
            bot.send_photo(message.chat.id,
                           images[0],
                           msg[:1000],
                           parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, e)

    else:
        try:
            bot.reply_to(message,
                         msg,
                         parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, e)
