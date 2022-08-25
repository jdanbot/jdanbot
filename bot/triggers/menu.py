from aiogram import types

from ..config import _, dp

buttons = ["main", "network", "wiki", "settings", "admin", "system", "notes", "pidor"]


def generate_keyboard_grid(
    buttons: list[str], selected_button: str
) -> types.InlineKeyboardMarkup:
    """Makes 2x2 keyboard grid

    Buttons list must be divisible by 2
    """

    keyboard = types.InlineKeyboardMarkup()
    btn_dict = _("menu.buttons")

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
        keyboard.add(*a)

    return keyboard


@dp.message_handler(commands=["start", "help"])
async def menu(message: types.Message):
    await message.reply(
        _("menu.main"),
        parse_mode="Markdown",
        reply_markup=generate_keyboard_grid(buttons, "main"),
        disable_web_page_preview=True,
    )


@dp.callback_query_handler(lambda call: call.data in buttons)
async def callback_worker(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        _(f"menu.{call.data}"),
        parse_mode="Markdown",
        reply_markup=generate_keyboard_grid(buttons, call.data),
        disable_web_page_preview=True,
    )
