import roman
from aiogram import types
from aiogram.filters import Command

from ..config import Locale, router
from ..filters import GetText


@router.message(
    Command("nvm", "rom"),
    GetText(disable_reply=True),
)
async def rmvn_empre(
    message: types.Message, query: str, _: Locale
):
    try:
        query_int = int(query)
    except ValueError:
        await message.reply(
            "only normal int`s", parse_mode=None
        )

    await message.reply(roman.toRoman(query_int))
