from aiogram import types

from .lib.monobank import MonobankApi
from ..config import dp


@dp.message_handler(commands=["mono"])
async def monobank(message: types.Message):
    mono = MonobankApi()
    currencies = await mono.get_currencies()

    msg = ""

    for currency in currencies:
        if currency.from_currency not in (840, 978, 643) or currency.to_currency != 980:
            continue

        msg += '{} ⇆ {}\n→ {} ₴\n← {} ₴\n\n'.format(
            currency.from_emoji,
            currency.to_emoji,
            currency.rate_buy or currency.rate_cross,
            currency.rate_sell or currency.rate_cross
        )

    await message.reply(msg)
