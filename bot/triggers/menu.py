from aiogram import types, F

from aiogram.filters import Command
from ..config import Locale, router


buttons = [
    "main",
    "network",
    "wiki",
    "settings",
    "admin",
    "system",
    "notes",
    "pidor",
]


def update_menu_buttons(_: Locale) -> list:
    return [getattr(_.btn, btn)() for btn in buttons]


def generate_keyboard_grid(
    buttons: list[str], _: Locale, selected_button: str
) -> types.InlineKeyboardMarkup:
    """Makes 2x2 keyboard grid

    Buttons list must be divisible by 2
    """

    btn_dict = update_menu_buttons(_)
    buttons = []

    btns = [
        types.InlineKeyboardButton(
            text=(
                btn_dict[button]
                if button != selected_button
                else "✅ " + btn_dict[button].split(maxsplit=1)[1]
            ),
            callback_data=button,
        )
        for button in buttons
    ]

    for ind, __ in enumerate(btns):
        a = btns[ind : ind + 2]
        btns.remove(a[1])
        buttons.append(a)

    return types.InlineKeyboardMarkup(keyboard=buttons)


@router.message(Command("start", "help"))
async def menu(
    message: types.Message,
):
    await message.reply(
        _("menu.main"),
        parse_mode="Markdown",
        reply_markup=generate_keyboard_grid(buttons, _, "main"),
        disable_web_page_preview=True,
    )


@router.callback_query(F.data.in_(buttons))
async def callback_worker(
    call: types.CallbackQuery, _: Locale
):
    await call.message.edit_text(
        _(f"menu.{call.data}"),
        parse_mode="Markdown",
        reply_markup=generate_keyboard_grid(buttons, _, call.data),
        disable_web_page_preview=True,
    )
    await call.answer()
