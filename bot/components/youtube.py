from .token import bot
import urllib


@bot.message_handler(commands=["preview"])
def preview(message):
    try:
        try:
            bot.send_chat_action(message.chat.id, "upload_photo")

            bot.send_photo(message.chat.id, f"https://img.youtube.com/vi/{message.reply_to_message.text.replace('&feature=share', '').split('/')[-1]}/maxresdefault.jpg")
        except:
            bot.send_chat_action(message.chat.id, "upload_photo")

            bot.send_photo(message.chat.id,
                           f'https://img.youtube.com/vi/{urllib.parse.parse_qs(urllib.parse.urlparse(message.reply_to_message.text).query)["v"][0]}/maxresdefault.jpg')
    except Exception as e:
        print(e)
        bot.reply_to(message, "Не получилось скачать превью")
