from ..config import bot, dp
from ..data import data

from random import choice


@dp.message_handler(commands=["pizda"])
async def pizda(message):
    await sendSticker(message, data.stickers.pizda)


@dp.message_handler(commands=["net_pizdy"])
async def net_pizdy(message):
    await sendSticker(message, data.stickers.net_pizdy)


@dp.message_handler(commands=["pizda_tebe"])
async def pizda_tebe(message):
    await sendSticker(message, data.stickers.pizda_tebe)


@dp.message_handler(commands=["xui"])
async def xui(message):
    await sendSticker(message, data.stickers.xui)


@dp.message_handler(commands=["net_xua"])
async def net_xua(message):
    await sendSticker(message, data.stickers.net_xua)


@dp.message_handler(commands=["xui_pizda"])
async def xui_pizda(message):
    sticker = choice([data.stickers.xui, data.stickers.pizda])
    await sendSticker(message, sticker)


async def sendSticker(message, sticker_id):
    try:
        await message.delete()
    except Exception:
        pass

    try:
        replied_id = message.reply_to_message.message_id
        await bot.send_sticker(message.chat.id, sticker_id,
                               reply_to_message_id=replied_id)
    except AttributeError:
        await bot.send_sticker(message.chat.id, sticker_id)
