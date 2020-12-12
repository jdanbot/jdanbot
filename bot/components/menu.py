from .token import bot
from .texts import texts

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
    buttons[ind] = telebot.types.InlineKeyboardButton(text=button[0],
                                                      callback_data=button[1])

for ind, button in enumerate(buttons):
    a = buttons[ind:ind + 2]
    try:
        buttons.remove(a[1])
    except:
        pass
    keyboard.add(*a)


@bot.message_handler(["new_menu", "start", "help"])
def menu(message):
    bot.reply_to(message,
                 texts["menu"]["main"],
                 parse_mode="HTML",
                 reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "main":
        edit(call, texts["menu"]["main"])

    if call.data == "math":
        edit(call, texts["menu"]["math"])

    if call.data == "text":
        edit(call, texts["menu"]["text"])

    if call.data == "network":
        edit(call, texts["menu"]["network"])

    if call.data == "math":
        edit(call, texts["menu"]["math"])

    if call.data == "images":
        edit(call, texts["menu"]["images"])

    if call.data == "commands":
        edit(call, texts["menu"]["commands"])

    if call.data == "crypt":
        edit(call, texts["menu"]["crypt"])

    if call.data == "memes":
        edit(call, texts["menu"]["memes"])


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
