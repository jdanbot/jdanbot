from aiogram import types

from ..config import dp
from ..lib.aioget import aioget


CURRENCIES = {
    840: "🇺🇸",
    980: "🇺🇦",
    978: "🇪🇺",
    643: "🇷🇺",
    985: "🇵🇱"
}


MONOBANK_LAST_REQUEST = {}


def get_emoji(code: int) -> str:
    emoji = CURRENCIES.get(code)
    return emoji if emoji is not None else code


@dp.message_handler(commands=["mono"])
async def monobank(message: types.Message):
    res = await aioget("https://api.monobank.ua/bank/currency")
    msg, cur = "", res.json()

    if isinstance(cur, list):
        global MONOBANK_LAST_REQUEST
        MONOBANK_LAST_REQUEST = cur

    for info in MONOBANK_LAST_REQUEST[::2][:3]:
        msg += '{} ⇆ {}\n→ {} ₴\n← {} ₴\n\n'.format(
            get_emoji(info["currencyCodeA"]),
            get_emoji(info["currencyCodeB"]),
            info.get("rateBuy"),
            info.get("rateSell")
        )

    await message.reply(msg)
