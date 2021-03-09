import aiogram

from .config import bot, dp
from .locale import locale

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

for ind, _button in enumerate(buttons):
    a = buttons[ind:ind + 2]
    buttons.remove(a[1])
    keyboard.add(*a)


@dp.message_handler(commands=["new_menu", "start", "help"])
async def menu(message):
    await message.reply(locale.menu.main, parse_mode="HTML",
                        reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True and
                           call.data in list(locale.menu.__dict__.keys()))
async def callback_worker(call):
    await edit(call, locale.menu.__dict__[call.data])


async def edit(call, text):
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text, parse_mode="HTML",
                                reply_markup=keyboard)
