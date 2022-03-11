from aiogram import types

from ..config import _, bot, dp
from .. import handlers


@dp.message_handler(commands=["admins"])
@handlers.check("__enable_admin__")
async def call_admins(message):
    # TODO: REWRITE: move keyboard to keyboards.py

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text=_("triggers.yes_"),
                                   callback_data="call_admin"),

        types.InlineKeyboardButton(text=_("triggers.delete"),
                                   callback_data="delete"))

    await message.reply(_("triggers.call_admin_warn"),
                        reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == "call_admin")
async def call_admin(call):
    # TODO: REWRITE: move keyboard to keyboards.py

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=_("triggers.delete"),
                                            callback_data="delete"))

    admins = await bot.get_chat_administrators(call.message.chat.id)
    usernames = [admin.user.get_mention(as_html=True) for admin in admins]
    admins_call = ", ".join(usernames) + "\n\n"

    await call.message.edit_text(
        text=admins_call + _("triggers.admins_called"),
        reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data == "delete")
async def delete_call(call):
    await call.message.delete()
