from .token import bot
from random import choice


@bot.message_handler(commands=["pizda"])
def pizda(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ")


@bot.message_handler(commands=["tebe_pizda"])
def tebe_pizda(message):
    sendSticker(message,
                "CAACAgIAAxkBAAILHV9qcv047Lzwp_B64lDlhtOD-2RGAAIgAgAClJlpL5VCBwPTI85YGwQ")


@bot.message_handler(commands=["net_pizdy"])
def net_pizdy(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQ1fCFkcDHIDN_h0qHDu7LgvS8SBIgAC4AADlJlpL8ZF00AlPORXGgQ")


@bot.message_handler(commands=["xui"])
def xui(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ")


@bot.message_handler(commands=["net_xua"])
def net_xua(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQ9fCFkfgfI9pH9Hr96q7dH0biVjEwAC4gADlJlpL_foG56vPzRPGgQ")


@bot.message_handler(commands=["xui_pizda"])
def xui_pizda(message):
    sendSticker(message,
                choice(["CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ", "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ"]))


def sendSticker(message, sticker_id):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_sticker(message.chat.id,
                         sticker_id,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_sticker(message.chat.id, sticker_id)
