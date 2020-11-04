from .token import bot
from .lib.lurkmore import Lurkmore


@bot.message_handler(["fallout"])
def fallout(message):
    f = Lurkmore()
    f.url = "https://fallout.fandom.com/ru/api.php"
    f.url2 = "https://fallout.fandom.com/ru/"
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        bot.reply_to(message, "Напишите название статьи")
        return

    name = options[1]
    print(f"[Fandom: Fallout] {name}")

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
