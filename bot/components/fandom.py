from .token import bot
from .lib.lurkmore import Lurkmore


@bot.message_handler(["fallout"])
def fallout(message):
    fandom(message, "Fallout", "https://fallout.fandom.com/ru/api.php")


@bot.message_handler(["doom"])
def doom(message):
    fandom(message, "DooM", "https://doom.fandom.com/ru/api.php")


def fandom(message, fname, url):
    f = Lurkmore()
    f.url = url
    f.url2 = url.replace("api.php", "")
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        bot.reply_to(message, "Напишите название статьи")
        return

    name = options[1]
    print(f"[Fandom: {fname}] {name}")

    s = f.opensearch(name)

    if len(s) == 0:
        bot.reply_to(message, "Не удалось найти статью")
        return

    p = f.getPage(s)
    i = f.getImageFromFandomPage(p)
    # for item in i:
    #     bot.send_photo(message.chat.id, lurk.getImage(item), caption=item)

    if i != 404:
        try:
            bot.send_chat_action(message.chat.id, "upload_photo")
            bot.send_photo(message.chat.id,
                           i,
                           caption=f.parse(p)[:1000],
                           reply_to_message_id=message.message_id,
                           parse_mode="HTML")
        except Exception as e:
            bot.send_chat_action(message.chat.id, "typing")
            # bot.reply_to(message, e)
            try:
                bot.reply_to(message, f.parse(p)[:4096], parse_mode="HTML")
            except:
                bot.reply_to(message, f.parse(p)[:4096])
    else:
        bot.reply_to(message, f.parse(p)[:4096], parse_mode="HTML")
