from ..config import dp, LANGS, _
from ..config.i18n import i18n

from ..schemas import Note, ChatMember

from .settings import settings_
from .modules import modules_

from aiogram import types


@dp.callback_query_handler(lambda call: call.data == "set_lang")
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
        callback_data="settings"
    ))

    await message.edit_text(
        _("settings.language_text"),
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: call.data == "set_reactions")
async def test(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    message = call.message

    btns = []

    for a, b in (("3", "⚠️ Отключить всё"), ("5", "⚠️ Удалять жоины")):
        btns.append(types.InlineKeyboardButton(
            b, callback_data=a
        ))

    kb.row(*btns)

    btns = []

    for a, b in (("3", "⚠️ Приветствие"), ("5", "⚠️ Изменить")):
        btns.append(types.InlineKeyboardButton(
            b, callback_data=a
        ))

    kb.row(*btns)

    btns = []

    for a, b in (("3", "⚠️ Правила"), ("5", "⚠️ Изменить")):
        btns.append(types.InlineKeyboardButton(
            b, callback_data=a
        ))

    kb.row(*btns)

    kb.add(types.InlineKeyboardButton(
        _("settings.button_back"),
        callback_data="settings"
    ))

    await message.edit_text(
        _("settings.reactions_text"),
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: call.data == "set_warn_count")
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
        callback_data="settings"
    ))

    await message.edit_text(
        _("settings.warns_to_ban_text"),
        reply_markup=kb
    )


@dp.callback_query_handler(lambda call: call.data.startswith("set "))
async def test(call: types.CallbackQuery):
    message = call.message
    member = ChatMember.get_by_message(message)

    __, section, key, value = call.data.split(maxsplit=4)

    await Note.add(member, key, value, is_admin_note=True)

    call.data = section

    if call.data == "settings":
        await settings_(call)
    elif call.data == "modules":
        await modules_(call)
