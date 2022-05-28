from aiogram import types, utils

from ..config import bot, dp, _


buttons = [
    "main", "math", "network",
    "text", "images", "commands",
    "crypt", "memes"
]


def generate_menu_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    btns = [types.InlineKeyboardButton(
                text=_(f"menu.buttons")[button],
                callback_data=button
            ) for button in buttons]

    for ind, __ in enumerate(btns):
        a = btns[ind:ind + 2]
        btns.remove(a[1])
        keyboard.add(*a)

    return keyboard


@dp.message_handler(commands=["new_menu", "start", "help"])
async def menu(message: types.Message):
    await message.reply(_("menu.main"), parse_mode="HTML",
                        reply_markup=generate_menu_keyboard(),
                        disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: True and call.data in buttons)
async def callback_worker(call):
    await call.answer()
    await edit(call, _(f"menu.{call.data}"))


async def edit(call, text: str):
    try:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text, parse_mode="HTML",
            reply_markup=generate_menu_keyboard(),
            disable_web_page_preview=True
        )
    except utils.exceptions.MessageNotModified:
        pass
