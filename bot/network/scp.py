import pyscp

from ..config import dp, logging
from ..lib import handlers
from ..lib.cutecrop import cuteCrop
from ..lib.fixHTML import fixHTML
from ..lib.html import bold, code 


def format_scp(p):
    text = p.text

    text = fixHTML(text)
    text = text.split("\n")

    # print("\n\n".join(text))

    try:
        for number, string in enumerate(text):
            if string.find("рейтинг:") != -1:
                del(text[number])

        for number, string in enumerate(text):
            test = ["Объект №:",
                    "Класс объекта:",
                    "Примеры объектов:",
                    "Описание:",
                    "Особые условия содержания:"]
            for k in test:
                if string.find(k) != -1:
                    o = string.split(":")[0]
                    text[number] = text[number].replace(o, bold(o))

        if text[0] == "":
            del(text[0])

        if len(p.images) != 0:
            del(text[0])

    #     text = "\n".join(text[:u])

    except Exception as e:
        print(e)

    text = cuteCrop("\n".join(text), 4096)

    title = fixHTML(p.title.replace('\n', ''))
    msg = f"<b>{title}</b>\n\n{text}"
    msg = msg.replace("</b>\n\n<b>", "</b>\n<b>")
    return msg


@dp.message_handler(commands=["scp"])
@handlers.parse_arguments(1)
async def detectscp(message, params):
    scp = pyscp.wikidot.Wiki('http://scpfoundation.net')
    logging.info(f"[SCP RU] {params[1]}")

    try:
        p = scp(params[1])
        p.title

    except AttributeError:
        try:
            p = scp("scp-" + params[1])
            p.title
        except AttributeError:
            await message.reply(bold("Не удалось найти scp"),
                                parse_mode="HTML")
            return

    images = p.images
    msg = format_scp(p)

    if len(images) != 0:
        try:
            await message.reply_photo(images[0], msg[:1024],
                                      parse_mode="HTML")
        except Exception as e:
            await message.reply(code(e), parse_mode="HTML")

    else:
        try:
            await message.reply(msg[:4096], parse_mode="HTML")
        except Exception as e:
            await message.reply(e)
