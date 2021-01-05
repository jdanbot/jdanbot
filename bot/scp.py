from .bot import dp
from .lib.html import code, bold
from .lib.fixHTML import fixHTML
import pyscp
import re


def format_scp(p):
    text = p.text

    # text = re.sub(r"рейтинг: ", "", p.text)

    text = fixHTML(text)
    text = re.sub(r"(\n\n\n|\n\n)", "\n", text)
    text = text.split("\n")

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
            test = ["Объект №:", "Класс объекта:",
                    "Примеры объектов:", "Описание:"]
            for k in test:
                if string.find(k) != -1:
                    o = string.split(":")[0]
                    text[number] = text[number].replace(o, bold(o))

            if "Описание:" in string:
                u = number + 1
            else:
                u = 6

        for number, string in enumerate(text):
            if string.startswith("Дополнение"):
                del(text[number])

        if text[0] == "":
            del(text[0])

        if len(p.images) != 0:
            del(text[0])

        text = "\n".join(text[:u])

    except Exception as e:
        print(e)
        text = "\n".join(text)

    title = fixHTML(p.title.replace('\n', ''))
    msg = f"<b>{title}</b>\n{text}"
    msg = msg.replace("</b>\n\n<b>", "</b>\n<b>")
    return msg


@dp.message_handler(commands=["scp"])
async def detectscp(message):
    scp = pyscp.wikidot.Wiki('http://scpfoundation.net')
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        await message.reply("Напишите название scp")
        return

    print(f"[SCP RU] {options[1]}")

    try:
        p = scp(options[1])
        p.title

    except AttributeError:
        try:
            p = scp("scp-" + options[1])
            p.title
        except AttributeError:
            await message.reply(bold("Не удалось найти scp"),
                                parse_mode="HTML")
            return

    images = p.images
    msg = format_scp(p)
    # print(msg)

    if len(images) != 0:
        try:
            await message.reply_photo(images[0], msg[:2048],
                                      parse_mode="HTML")
        except Exception as e:
            await message.reply(code(e), parse_mode="HTML")

    else:
        try:
            await message.reply(msg[:4096], parse_mode="HTML")
        except Exception as e:
            await message.reply(e)
