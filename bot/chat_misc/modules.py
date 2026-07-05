from aiogram import F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import Locale, router
from ..database import ChatSettings, Member
from ..filters import IsAdmin


def generate_modules_list(
    settings: ChatSettings, _: Locale
):
    return (
        (settings.enable_admin, _.modules.admin, True),
        (settings.enable_selfmute, _.modules.selfmute),
        (settings.enable_kick_on_join, "polyak!"),
        (settings.enable_twitter_redirect, "twi"),
        (
            settings.enable_extra_poll_option,
            "inline note settin'",
        ),
        (
            settings.enable_extra_poll_option,
            "extra poll option",
        ),
        (True, "padding!"),
        (False, "Test Section!"),
    )


@router.message(Command("modules_beta"), IsAdmin())
@router.callback_query(F.data == "modules_beta", IsAdmin())
async def modules_(
    message: types.Message, member: Member, _: Locale
):
    try:
        message: types.Message = message.message
        is_inline = True
    except Exception:
        is_inline = False

    kb = InlineKeyboardBuilder()

    chat = member.chat
    modules = chat.settings

    bools = {False: "❌", True: "✅"}

    for btn in generate_modules_list(
        member.chat.settings, _
    ):
        print(btn[2:3] or None)
        kb.button(
            text=f"{bools[btn[0]]} {btn[1]}",
            callback_data="test",
            style="success" if btn[2:3] else None,
        )

    kb.button(
        text=_.settings.done,
        callback_data="modules_beta",
        style="primary",
    )

    params = dict(
        text="settings.modules_text",
        reply_markup=kb.adjust(1, 2, 2, 2, 1).as_markup(),
        parse_mode=None,
    )

    if is_inline:
        await message.edit_text(_**params)
    else:
        await message.answer(**params)
        await message.delete()

    return
    kb.button(
        text=f"{bools[modules.enable_admin]} {_('settings.admin')}",
        callback_data=f"set modules __enable_admin__ {not modules.enable_admin}",
    )
    kb.button(
        text=f"⚠️ {_('settings.mute')}",
        callback_data="test",
    )

    kb.button(
        text=f"⚠️ {_('settings.warn')}", callback_data="test"
    )

    kb.button(
        text=f"{bools[modules.is_selfmute_enabled]} {_('settings.selfmute')}",
        callback_data=f"set modules __enable_selfmute__ {not modules.is_selfmute_enabled}",
    )
    kb.button(
        text=f"{bools[modules.is_poll_enabled]} {_('settings.polls')}",
        callback_data=f"set modules enable_poll {not modules.is_poll_enabled}",
    )
    kb.add(
        types.InlineKeyboardButton(
            f"{bools[modules.is_memes_enabled]} {_('settings.memes')}",
            callback_data=f"set modules __enable_response__ {not modules.is_memes_enabled}",
        )
    )
    kb.row(
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.stickers')}",
            callback_data="test",
        ),
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.text_memes')}",
            callback_data="test",
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.eggs')}", callback_data="test"
        ),
        types.InlineKeyboardButton(
            f"{bools[modules.is_ban_enabled]} {_('settings.ban')}",
            callback_data=f"set modules enable_ban_trigger {not modules.is_ban_enabled}",
        ),
    )
    kb.row(
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.ban2')}", callback_data="test"
        ),
        types.InlineKeyboardButton(
            f"⚠️ {_('settings.boikot')}",
            callback_data="test",
        ),
    )
