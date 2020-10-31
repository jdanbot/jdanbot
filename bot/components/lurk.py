from .token import bot
from .lib.lurkmore import Lurkmore

lurk = Lurkmore()


@bot.message_handler(commands=["lurk"])
def getlurk(message, logs=False):
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        bot.reply_to(message, "Напишите название статьи")
        return

    name = options[1]
    print(f"[Lurkmore] {name}")

    s = lurk.opensearch(name)

    if len(s) == 0:
        bot.reply_to(message, "Не найдено")
        return

    p = lurk.getPage(s)
    i = lurk.getImagesList(s)

    # for item in i:
    #     bot.send_photo(message.chat.id, lurk.getImage(item), caption=item)

    if len(i) != 0:
        try:
            image = lurk.getImage(i[0])
            bot.send_chat_action(message.chat.id, "upload_photo")
            bot.send_photo(message.chat.id,
                           image,
                           caption=lurk.parse(p)[:1000],
                           parse_mode="HTML")
        except Exception as e:
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(message, e)
            try:
                bot.reply_to(message, lurk.parse(p)[:4096], parse_mode="HTML")
            except:
                bot.reply_to(message, lurk.parse(p)[:4096])
    else:
        bot.reply_to(message, lurk.parse(p)[:4096], parse_mode="HTML")
