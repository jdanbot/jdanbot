from ..config import dp, _
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
            f"{bools[modules.is_admin_enabled]} {_('settings.admin')}",
            callback_data=f"set modules __enable_admin__ {not modules.is_admin_enabled}"
        )
    )
    kb.row(
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.mute')}",
            callback_data="test"
        ),

        types.InlineKeyboardButton(
            f"⚠️ {_('settings.warn')}",
            callback_data="test"
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            f"{bools[modules.is_selfmute_enabled]} {_('settings.selfmute')}",
            callback_data=f"set modules __enable_selfmute__ {not modules.is_selfmute_enabled}"
        ),

        types.InlineKeyboardButton(
            f"{bools[modules.is_poll_enabled]} {_('settings.polls')}",
            callback_data=f"set modules enable_poll {not modules.is_poll_enabled}"
        ),
    )
    kb.add(
        types.InlineKeyboardButton(
            f"{bools[modules.is_memes_enabled]} {_('settings.memes')}",
            callback_data=f"set modules __enable_response__ {not modules.is_memes_enabled}"
        )
    )
    kb.row(
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.stickers')}",
            callback_data="test"
        ),
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.text_memes')}",
            callback_data="test"
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.eggs')}",
            callback_data="test"
        ),

        types.InlineKeyboardButton(
            f"{bools[modules.is_ban_enabled]} {_('settings.ban')}",
            callback_data=f"set modules enable_ban_trigger {not modules.is_ban_enabled}"
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.ban2')}",
            callback_data="test"
        ),

        types.InlineKeyboardButton(
            f"⚠️ {_('settings.boikot')}",
            callback_data="test"
        ),
    )

    kb.add(types.InlineKeyboardButton(
        _("settings.done"),
        callback_data="delete_msg"
    ))

    if is_inline:
        await message.edit_text(_("settings.modules_text"), reply_markup=kb)
    else:
        await message.answer(_("settings.modules_text"), reply_markup=kb)
        await message.delete()
