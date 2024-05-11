from aiogram import types, F

from aiogram.filters import Command
from ..config import LANGS, _, router
from ..database import Member, Note
from .modules import modules_
from .settings import settings_
from fluentogram import TranslatorRunner
from ..filters import IsAdmin


@router.callback_query(F.data == "set_lang", IsAdmin())
async def test(call: types.CallbackQuery, _: TranslatorRunner):
    try:
        message = call.message
    except AttributeError:
        message = call

    buttons = [
        *[
            [
                types.InlineKeyboardButton(
                    text=f"{LANGS[lang].emoji} {LANGS[lang].name}",
                    callback_data=f"set settings __chat_lang__ {lang}",
                )
            ]
            for lang in ("ru", "en")
        ],
        [
            types.InlineKeyboardButton(
                text=_.button_back(),
                callback_data="settings_menu",
            )
        ],
    ]

    await message.edit_text(
        _.language_text(),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
    )


@router.callback_query(F.data == "set_reactions", IsAdmin())
async def test(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()

    try:
        message = call.message
    except:
        message = call

    btns = []

    for a, b in (
        ("3", f"⚠️ {_('settings.disable_all_reactions')}"),
        ("5", f"⚠️ {_('settings.disable_join_message')}"),
    ):
        btns.append(types.InlineKeyboardButton(b, callback_data=a))

    kb.row(*btns)

    btns = []

    for a, b in (
        ("3", f"⚠️ {_('settings.welcome')}"),
        ("5", f"⚠️ {_('settings.edit')}"),
    ):
        btns.append(types.InlineKeyboardButton(b, callback_data=a))

    kb.row(*btns)

    btns = []

    for a, b in (
        ("3", f"⚠️ {_('settings.rules')}"),
        ("5", f"⚠️ {_('settings.edit')}"),
    ):
        btns.append(types.InlineKeyboardButton(b, callback_data=a))

    kb.row(*btns)

    kb.add(
        types.InlineKeyboardButton(
            _("settings.button_back"), callback_data="settings_menu"
        )
    )

    await message.edit_text(
        _("settings.reactions_text"), reply_markup=kb
    )


@router.callback_query(F.data == "set_warn_count", IsAdmin())
async def test(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    message = call.message

    btns = []

    for a, b in (("3", "3️⃣"), ("5", "5️⃣"), ("-1", "⛔️")):
        btns.append(
            types.InlineKeyboardButton(
                b, callback_data=f"set settings __warns_to_ban__ {a}"
            )
        )

    kb.row(*btns)

    kb.add(
        types.InlineKeyboardButton(
            _("settings.button_back"), callback_data="settings_menu"
        )
    )

    await message.edit_text(
        _("settings.warns_to_ban_text"), reply_markup=kb
    )


@router.callback_query(F.data.startswith("set "), IsAdmin())
async def test(call: types.CallbackQuery, _: TranslatorRunner):
    message = call.message
    member = await Member.get_by(message)

    __, section, key, value = call.data.split(maxsplit=4)

    await Note.add(member, key, value, is_admin_note=True)

    if section == "settings":
        await settings_(
            call.model_copy(update={"data": "settings_menu"}),
            _=_,
        )
    elif section == "modules":
        await modules_(
            call.model_copy(update={"data": "modules"}),
            _=_,
        )
