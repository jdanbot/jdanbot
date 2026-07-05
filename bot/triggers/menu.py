import msgspec
from aiogram import F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import Locale, router

MENU_BUTTONS = list(Locale.Menu.MenuButtons.__annotations__)


def generate_keyboard_grid(
    selected_button: str, _: Locale
) -> types.InlineKeyboardMarkup | types.ReplyKeyboardMarkup:
    """Makes 2x2 keyboard grid"""

    buttons = msgspec.to_builtins(_.menu.buttons)
    keyboard = InlineKeyboardBuilder()

    for button, label in buttons.items():
        is_selected = button == selected_button

        keyboard.button(
            text=f"✅ {label.split(maxsplit=1)[1]}"
            if is_selected
            else label,
            callback_data=button,
            style="success" if is_selected else None,
        )

    return keyboard.adjust(2, repeat=True).as_markup()


@router.message(Command("start", "help"))
async def menu(message: types.Message, _: Locale):
    await message.reply(
        _.menu.main,
        parse_mode="Markdown",
        reply_markup=generate_keyboard_grid("main", _),
        disable_web_page_preview=True,
    )


@router.callback_query(F.data.in_(MENU_BUTTONS))
async def callback_worker(
    call: types.CallbackQuery, _: Locale
):
    assert call.data

    await call.message.edit_text(
        getattr(_.menu, call.data),
        parse_mode="Markdown",
        reply_markup=generate_keyboard_grid(call.data, _),
        disable_web_page_preview=True,
    )
    await call.answer()
