from .config import dp, bot
from .data import data

import aiogram


keyboard = aiogram.types.InlineKeyboardMarkup()

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
    buttons[ind] = aiogram.types.InlineKeyboardButton(text=button[0],
                                                      callback_data=button[1])

for ind, button in enumerate(buttons):
    a = buttons[ind:ind + 2]
    buttons.remove(a[1])
    keyboard.add(*a)


@dp.message_handler(commands=["new_menu", "start", "help"])
async def menu(message):
    await message.reply(data["menu"]["main"], parse_mode="HTML",
                        reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True)
async def callback_worker(call):
    if call.data == "main":
        await edit(call, data["menu"]["main"])

    if call.data == "math":
        await edit(call, data["menu"]["math"])

    if call.data == "text":
        await edit(call, data["menu"]["text"])

    if call.data == "network":
        await edit(call, data["menu"]["network"])

    if call.data == "math":
        await edit(call, data["menu"]["math"])

    if call.data == "images":
        await edit(call, data["menu"]["images"])

    if call.data == "commands":
        await edit(call, data["menu"]["commands"])

    if call.data == "crypt":
        await edit(call, data["menu"]["crypt"])

    if call.data == "memes":
        await edit(call, data["menu"]["memes"])


async def edit(call, text):
    try:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=text, parse_mode="HTML",
                                    reply_markup=keyboard)
    except Exception:
        pass
