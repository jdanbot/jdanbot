from ..config import dp
from ..schemas import Chat

from aiogram import types


@dp.message_handler(commands="modules_beta")
@dp.callback_query_handler(lambda call: call.data == "modules")
async def modules_(message: types.Message):
    try:
        message: types.Message = message.message
        is_inline = True
    except:
        is_inline = False

    kb = types.InlineKeyboardMarkup()

    chat = Chat.get_by_message(message)
    modules = chat.get_modules()

    bools = {False: "❌", True: "✅"}

    kb.add(
        types.InlineKeyboardButton(
            f"{bools[modules.is_admin_enabled]} Админка",
            callback_data=f"set modules __enable_admin__ {not modules.is_admin_enabled}"
        )
    )
    kb.row(
        types.InlineKeyboardButton(
            "⚠️ Муты",
            callback_data="test"
        ),

        types.InlineKeyboardButton(
            "⚠️ Преды",
            callback_data="test"
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            f"{bools[modules.is_selfmute_enabled]} Самомут",
            callback_data=f"set modules __enable_selfmute__ {not modules.is_selfmute_enabled}"
        ),

        types.InlineKeyboardButton(
            f"{bools[modules.is_poll_enabled]} Опросы",
            callback_data=f"set modules enable_poll {not modules.is_poll_enabled}"
        ),
    )
    kb.add(
        types.InlineKeyboardButton(
            f"{bools[modules.is_memes_enabled]} Мемы",
            callback_data=f"set modules __enable_response__ {not modules.is_memes_enabled}"
        )
    )
    kb.row(
        types.InlineKeyboardButton(
            "⚠️ Стикеры",
            callback_data="test"
        ),
        types.InlineKeyboardButton(
            "⚠️ Текстовые мемы",
            callback_data="test"
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            "⚠️ Пасхалки",
            callback_data="test"
        ),

        types.InlineKeyboardButton(
            f"{bools[modules.is_ban_enabled]} Бан",
            callback_data=f"set modules enable_ban_trigger {not modules.is_ban_enabled}"
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            "⚠️ Бан2",
            callback_data="test"
        ),

        types.InlineKeyboardButton(
            "⚠️ Бойкот",
            callback_data="test"
        ),
    )

    if is_inline:
        await message.edit_reply_markup(kb)
    else:
        await message.answer("modules", reply_markup=kb)
        await message.delete()

