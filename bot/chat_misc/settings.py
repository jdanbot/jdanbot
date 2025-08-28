from aiogram import F, types
from aiogram.filters import Command

from ..config import LANGS, Locale, router
from ..database import Chat
from ..filters import IsAdmin


@router.message(Command("settings"), IsAdmin())
@router.callback_query(F.data == "settings_menu", IsAdmin())
async def settings_(message: types.Message, _: Locale):
    try:
        message: types.Message = message.message
        is_inline = True
    except Exception:
        is_inline = False

    chat = await Chat.get_by(message)
    settings = await chat.get_settings()

    buttons = [
        [
            types.InlineKeyboardButton(
                text=_.reactions(react=settings.reactions),
                callback_data="set_reactions",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_.warns_to_ban(warns=settings.warns_to_ban),
                callback_data="set_warn_count",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_.language(
                    lang=LANGS[settings.language or -1].emoji
                ),
                callback_data="set_lang",
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=_.done(), callback_data="delete_msg"
            ),
        ],
    ]

    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    if is_inline:
        await message.edit_text(
            text=_.settings_text(), reply_markup=kb
        )
    else:
        await message.answer(text=_.settings_text(), reply_markup=kb)
        await message.delete()


@router.callback_query(F.data == "delete_msg", IsAdmin())
async def test_(call: types.CallbackQuery):
    await call.message.delete()
