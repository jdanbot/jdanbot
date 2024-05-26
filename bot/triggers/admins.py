from aiogram import types, F

from aiogram.filters import Command
from ..config import bot, router
from ..filters import Check
from fluentogram import TranslatorRunner


@router.message(Command("admins"), Check("__enable_admin__"))
async def call_admins(message, _: TranslatorRunner):
    buttons = [
        [
            types.InlineKeyboardButton(
                text=_.triggers.yes_(), callback_data="call_admin"
            ),
            types.InlineKeyboardButton(
                text=_.triggers.delete(), callback_data="delete"
            ),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.reply(
        _.triggers.call_admin_warn(), reply_markup=keyboard
    )


@router.callback_query(F.data == "call_admin")
async def call_admin(call: types.CallbackQuery, _: TranslatorRunner):
    buttons = [
        [
            types.InlineKeyboardButton(
                text=_.triggers.delete(), callback_data="delete"
            )
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    admins = await bot.get_chat_administrators(call.message.chat.id)
    usernames = [admin.user.mention_html() for admin in admins]
    admins_call = ", ".join(usernames) + "\n\n"

    await call.message.edit_text(
        text=admins_call + _.triggers.admins_called(),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "delete")
async def delete_call(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()
