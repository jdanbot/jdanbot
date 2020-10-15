from .token import bot
from . import texts

import telebot


keyboard = telebot.types.InlineKeyboardMarkup()

buttons = [
    ["Главная", "main"],
    ["Математика", "math"],
    ["Онлайн-ресурсы", "network"],
    ["Работа с текстом", "text"],
    ["Работа с изображениями", "images"],
    ["Служебные команды", "commands"],
    ["Шифровая херня", "crypt"],
    ["Мемы", "memes"]
]

for ind, button in enumerate(buttons):
    buttons[ind] = telebot.types.InlineKeyboardButton(text=button[0], callback_data=button[1])

for ind, button in enumerate(buttons):
    a = buttons[ind:ind + 2]
    try:
        buttons.remove(a[1])
    except:
        pass
    keyboard.add(*a)


@bot.message_handler(["new_menu", "start", "help"])
def menu(message):
    bot.reply_to(message, texts.main, parse_mode="HTML", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "main":
        edit(call, texts.main)

    if call.data == "math":
        edit(call, texts.math)

    if call.data == "text":
        edit(call, texts.text)

    if call.data == "network":
        edit(call, texts.network)

    if call.data == "math":
        edit(call, texts.math)

    if call.data == "images":
        edit(call, texts.images)

    if call.data == "commands":
        edit(call, texts.commands)

    if call.data == "crypt":
        edit(call, texts.crypt)

    if call.data == "memes":
        edit(call, texts.memes)


def edit(call, text):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text,
                              parse_mode="HTML",
                              reply_markup=keyboard)
    except Exception as e:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Вы уже в этом пункте")
