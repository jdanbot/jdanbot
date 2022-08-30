from aiogram import types

from .. import handlers
from ..config import LANGS, _, dp
from ..schemas import Chat


@dp.message_handler(commands="settings_beta")
@dp.callback_query_handler(lambda call: call.data == "settings_menu")
@handlers.only_admins
async def settings_(message: types.Message):
    try:
        message: types.Message = message.message
        is_inline = True
    except:
        is_inline = False

    _(None, return_lang=True, force_reload=True)

    kb = types.InlineKeyboardMarkup()

    chat = Chat.get_by_message(message)
    settings = chat.get_settings()

    warns = {3: "3️⃣", 5: "5️⃣", -1: "⛔️"}
    reactions = {None: "☑️", False: "❌", True: "✅"}

    kb.add(types.InlineKeyboardButton(
        f"⚠️ {_('settings.reactions')}",
        callback_data="set_reactions"
    ))

    kb.add(types.InlineKeyboardButton(
        f"{warns[settings.warns_to_ban]} {_('settings.warns_to_ban')}",
        callback_data="set_warn_count"
    ))

    kb.add(types.InlineKeyboardButton(
        f"{LANGS[settings.language].emoji} {_('settings.language')}",
        callback_data="set_lang"
    ))

    kb.add(types.InlineKeyboardButton(
        _("settings.done"),
        callback_data="delete_msg"
    ))

    if is_inline:
        await message.edit_text(_("settings.settings_text"), reply_markup=kb)
    else:
        await message.answer(_("settings.settings_text"), reply_markup=kb)
        await message.delete()


@dp.callback_query_handler(lambda call: call.data == "delete_msg")
@handlers.only_admins
async def test_(call: types.CallbackQuery):
    await call.message.delete()
