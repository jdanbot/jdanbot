from aiogram import F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import LANGS, Locale, router
from ..database import Member
from ..filters import IsAdmin
from .modules import modules_
from .settings import settings_


def back(keyboard: InlineKeyboardBuilder, _: Locale):
    keyboard.button(
        text=_.settings.button_back,
        callback_data="settings_menu",
        style="primary",
    )


@router.message(Command("lang", "locale"), IsAdmin())
@router.callback_query(F.data == "set_lang", IsAdmin())
async def test(call: types.CallbackQuery, _: Locale):
    try:
        message: types.Message = call.message
        is_inline = True
    except Exception:
        message = call
        is_inline = False

    keyboard = InlineKeyboardBuilder()

    for lang in ("ru", "en", "uk"):
        keyboard.button(
            text=f"{LANGS[lang].emoji} {LANGS[lang].name}",
            callback_data=f"set settings lang {lang}",
        )

    back(keyboard, _)

    params = dict(
        text=_.settings.language_text,
        reply_markup=keyboard.adjust(
            1, repeat=True
        ).as_markup(),
    )

    if is_inline:
        await message.edit_text(**params)
    else:
        await message.answer(**params)
        await message.delete()


# YAML
# disable_all_reactions: Отключить все реакции
# disable_join_message: Удалять жоины

# welcome: Приветствие
# rules: Правила

# edit: Изменить
# -- YAML

# @router.callback_query(F.data == "set_reactions", IsAdmin())
# async def test_(call: types.CallbackQuery, _: Locale):
#     buttons = []

#     try:
#         message = call.message
#     except Exception:
#         message = call

#     btns = []

#     for a, b in (
#         ("3", f"⚠️ {_.disable_all_reactions()}"),
#         ("5", f"⚠️ {_.disable_join_message()}"),
#     ):
#         btns.append(
#             types.InlineKeyboardButton(
#                 text=b, callback_data=a
#             )
#         )

#     buttons.append(btns)

#     btns = []

#     for a, b in (
#         ("3", f"⚠️ {_.welcome()}"),
#         ("5", f"⚠️ {_.settings.edit()}"),
#     ):
#         btns.append(
#             types.InlineKeyboardButton(
#                 text=b, callback_data=a
#             )
#         )

#     buttons.append(btns)

#     btns = []

#     for a, b in (
#         ("3", f"⚠️ {_.rules()}"),
#         ("5", f"⚠️ {_.edit()}"),
#     ):
#         btns.append(
#             types.InlineKeyboardButton(
#                 text=b, callback_data=a
#             )
#         )

#     buttons.append(btns)

#     buttons.append(
#         [
#             types.InlineKeyboardButton(
#                 text=_.button_back(),
#                 callback_data="settings_menu",
#             )
#         ]
#     )

#     kb = types.InlineKeyboardMarkup(inline_keyboard=buttons)

#     await message.edit_text(
#         _.settings_text(), reply_markup=kb
#     )


@router.callback_query(
    F.data == "set_warn_count", IsAdmin()
)
async def test____(call: types.CallbackQuery, _: Locale):
    keyboard = InlineKeyboardBuilder()
    message = call.message

    for a, b in (("3", "3️⃣"), ("5", "5️⃣"), ("-1", "⛔️")):
        keyboard.button(
            text=b,
            callback_data=f"set settings warns_to_ban {a}",
        )

    back(keyboard, _)

    await message.edit_text(
        _.settings.warns_to_ban_text,
        reply_markup=keyboard.adjust(3, 1).as_markup(),
    )


@router.callback_query(F.data.startswith("set "), IsAdmin())
async def test__(call: types.CallbackQuery, _: Locale):
    message = call.message
    member = await Member.get_by(message)

    assert call.data
    __, section, key, value = call.data.split(maxsplit=4)

    if key == "lang":
        await member.chat.set_language(value)
    elif section == "settings_switch":
        setting = getattr(member.chat.settings, key)
        await member.chat.set_bool_setting(key, not setting)
    else:
        await member.chat.set_setting(key, value)

    if section in ["settings", "settings_switch"]:
        await settings_(
            call.model_copy(
                update={"data": "settings_menu"}
            ),
            _=_,
        )
    elif section == "modules":
        await modules_(
            call.model_copy(update={"data": "modules"}),
            _=_,
        )
