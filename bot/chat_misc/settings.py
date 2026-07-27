from aiogram import F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import LANGS, Locale, router
from ..database import Chat
from ..filters import IsAdmin


def unite(*args) -> str:
    return " ".join([*args])


@router.message(Command("settings"), IsAdmin())
@router.callback_query(F.data == "settings_menu", IsAdmin())
async def settings_(message: types.Message, _: Locale):
    try:
        message: types.Message = message.message
        is_inline = True
    except Exception:
        is_inline = False

    chat = await Chat.get_by(message)
    settings = chat.settings

    warns = {3: "3️⃣", 5: "5️⃣", -1: "⛔️"}
    reactions = {None: "☑️", False: "❌", True: "✅"}

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=unite(
            _.settings.reactions,
            reactions[settings.enable_triggers],
        ),
        callback_data="set settings_switch enable_triggers ignore",
    )
    keyboard.button(
        text=unite(
            _.settings.warns_to_ban,
            warns[settings.warns_to_ban],
        ),
        callback_data="set_warn_count",
    )
    keyboard.button(
        text=unite(
            _.settings.locale,
            LANGS[chat.language.alpha_2].emoji,
        ),
        callback_data="set_lang",
    )
    keyboard.button(
        text=_.settings.done,
        callback_data="delete_msg",
        style="primary",
    )

    kb = keyboard.adjust(1, repeat=True).as_markup()

    if is_inline:
        await message.edit_text(
            text=_.settings.settings_text, reply_markup=kb
        )
    else:
        await message.answer(
            text=_.settings.settings_text, reply_markup=kb
        )
        await message.delete()


@router.callback_query(F.data == "delete_msg", IsAdmin())
async def test_(call: types.CallbackQuery):
    await call.message.delete()
