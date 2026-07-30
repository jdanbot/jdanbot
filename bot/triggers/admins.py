from aiogram import F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import Locale, bot, router
from ..database.chat import ChatSettings
from ..filters import Check


@router.message(
    Command("admins"), Check(ChatSettings.enable_admin)
)
async def call_admins(message: types.Message, _: Locale):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=_.triggers.yes,
        callback_data="call_admin",
        style="danger",
    )
    keyboard.button(
        text=_.triggers.delete,
        callback_data="delete",
        style="success",
    )

    await message.reply(
        _.triggers.call_admin_warn,
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(F.data == "call_admin")
async def call_admin(call: types.CallbackQuery, _: Locale):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=_.triggers.delete,
        callback_data="delete",
        style="danger",
    )

    admins = await bot.get_chat_administrators(
        call.message.chat.id
    )
    usernames = [
        admin.user.mention_html() for admin in admins
    ]
    admins_call = ", ".join(usernames) + "\n\n"

    await call.message.edit_text(
        text=admins_call + _.triggers._admins_called,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(F.data == "delete")
async def delete_call(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()
