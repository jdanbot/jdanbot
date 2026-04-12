from aiogram import F, types
from aiogram.filters import Command

from ..config import Locale, bot, router
from ..database.chat import ChatSettings
from ..filters import Check
from ..triggers.legacy import triggers


@router.message(
    Command("admins"), Check(ChatSettings.enable_admin)
)
async def call_admins(message, _: Locale):
    buttons = [
        [
            types.InlineKeyboardButton(
                text=triggers["yes_"],
                callback_data="call_admin",
                style="danger",
            ),
            types.InlineKeyboardButton(
                text=triggers["delete"],
                callback_data="delete",
                style="success",
            ),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await message.reply(
        triggers["call_admin_warn"], reply_markup=keyboard
    )


@router.callback_query(F.data == "call_admin")
async def call_admin(call: types.CallbackQuery, _: Locale):
    buttons = [
        [
            types.InlineKeyboardButton(
                text=triggers["delete"],
                callback_data="delete",
            )
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    admins = await bot.get_chat_administrators(
        call.message.chat.id
    )
    usernames = [
        admin.user.mention_html() for admin in admins
    ]
    admins_call = ", ".join(usernames) + "\n\n"

    await call.message.edit_text(
        text=admins_call + triggers["admins_called"],
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "delete")
async def delete_call(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()
