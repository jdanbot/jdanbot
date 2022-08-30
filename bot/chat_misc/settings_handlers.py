from aiogram import types

from .. import handlers
from ..config import LANGS, _, dp
from ..config.i18n import i18n
from ..schemas import ChatMember, Note
from .modules import modules_
from .settings import settings_


@dp.callback_query_handler(lambda call: call.data == "set_lang")
@handlers.only_admins
async def test(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    message = call.message

    for lang in i18n.pyi18n.languages:
        kb.add(types.InlineKeyboardButton(
            f'{LANGS[lang].emoji} {LANGS[lang].name}',
            callback_data=f"set settings __chat_lang__ {lang}"
        ))

    kb.add(types.InlineKeyboardButton(
        _("settings.button_back"),
        callback_data="settings_menu"
    ))

    await message.edit_text(
        _("settings.language_text"),
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: call.data == "set_reactions")
@handlers.only_admins
async def test(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    message = call.message

    btns = []

    for a, b in (("3", f"⚠️ {_('settings.disable_all_reactions')}"), ("5", f"⚠️ {_('settings.disable_join_message')}")):
        btns.append(types.InlineKeyboardButton(
            b, callback_data=a
        ))

    kb.row(*btns)

    btns = []

    for a, b in (("3", f"⚠️ {_('settings.welcome')}"), ("5", f"⚠️ {_('settings.edit')}")):
        btns.append(types.InlineKeyboardButton(
            b, callback_data=a
        ))

    kb.row(*btns)

    btns = []

    for a, b in (("3", f"⚠️ {_('settings.rules')}"), ("5", f"⚠️ {_('settings.edit')}")):
        btns.append(types.InlineKeyboardButton(
            b, callback_data=a
        ))

    kb.row(*btns)

    kb.add(types.InlineKeyboardButton(
        _("settings.button_back"),
        callback_data="settings_menu"
    ))

    await message.edit_text(
        _("settings.reactions_text"),
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: call.data == "set_warn_count")
@handlers.only_admins
async def test(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    message = call.message

    btns = []

    for a, b in (("3", "3️⃣"), ("5", "5️⃣"), ("-1", "⛔️")):
        btns.append(types.InlineKeyboardButton(
            b, callback_data=f"set settings __warns_to_ban__ {a}"
        ))

    kb.row(*btns)

    kb.add(types.InlineKeyboardButton(
        _("settings.button_back"),
        callback_data="settings_menu"
    ))

    await message.edit_text(
        _("settings.warns_to_ban_text"),
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: call.data.startswith("set "))
@handlers.only_admins
async def test(call: types.CallbackQuery):
    message = call.message
    member = ChatMember.get_by_message(message)

    __, section, key, value = call.data.split(maxsplit=4)

    await Note.add(member, key, value, is_admin_note=True)

    call.data = section

    if call.data == "settings":
        call.data = "settings_menu"
        await settings_(call)
    elif call.data == "modules":
        await modules_(call)
