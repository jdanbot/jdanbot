from aiogram import F, types

from ..config import LANGS, Locale, router
from ..database import Member, Note
from ..filters import IsAdmin
from .modules import modules_
from .settings import settings_


@router.callback_query(F.data == "set_lang", IsAdmin())
async def test(call: types.CallbackQuery, _: Locale):
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
async def test(call: types.CallbackQuery, _: Locale):
    buttons = []

    try:
        message = call.message
    except Exception:
        message = call

    btns = []

    for a, b in (
        ("3", f"⚠️ {_.disable_all_reactions()}"),
        ("5", f"⚠️ {_.disable_join_message()}"),
    ):
        btns.append(
            types.InlineKeyboardButton(text=b, callback_data=a)
        )

    buttons.append(btns)

    btns = []

    for a, b in (
        ("3", f"⚠️ {_.welcome()}"),
        ("5", f"⚠️ {_.settings.edit()}"),
    ):
        btns.append(
            types.InlineKeyboardButton(text=b, callback_data=a)
        )

    buttons.append(btns)

    btns = []

    for a, b in (
        ("3", f"⚠️ {_.rules()}"),
        ("5", f"⚠️ {_.edit()}"),
    ):
        btns.append(
            types.InlineKeyboardButton(text=b, callback_data=a)
        )

    buttons.append(btns)

    buttons.append(
        [
            types.InlineKeyboardButton(
                text=_.button_back(), callback_data="settings_menu"
            )
        ]
    )

    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.edit_text(_.settings_text(), reply_markup=kb)


@router.callback_query(F.data == "set_warn_count", IsAdmin())
async def test(call: types.CallbackQuery, _: Locale):
    buttons = []
    message = call.message

    btns = []

    for a, b in (("3", "3️⃣"), ("5", "5️⃣"), ("-1", "⛔️")):
        btns.append(
            types.InlineKeyboardButton(
                text=b,
                callback_data=f"set settings __warns_to_ban__ {a}",
            )
        )

    buttons.append(btns)

    buttons.append(
        [
            types.InlineKeyboardButton(
                text=_.button_back(), callback_data="settings_menu"
            )
        ]
    )

    kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(_.warns_to_ban_text(), reply_markup=kb)


@router.callback_query(F.data.startswith("set "), IsAdmin())
async def test(call: types.CallbackQuery, _: Locale):
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
