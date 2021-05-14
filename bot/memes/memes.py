from ..config import bot, dp, _


async def send_meme(message, text):
    try:
        await message.delete()
    except Exception:
        pass

    try:
        await bot.send_message(
            message.chat.id, text,
            reply_to_message_id=message.reply_to_message.message_id
        )
    except AttributeError:
        await message.answer(text)


memes = {
    "bylo": "Было",
    "ne_bylo": "Не было",
    "rzaka": _("ban.rzaka"),
    "rzaka_full": _("ban.rzaka_full"),
    "rzaka_time": 848393938347292929647492918363739304964682010
}


@dp.message_handler(commands=["bylo"])
async def bylo(message):
    await send_meme(message, memes["bylo"])


@dp.message_handler(commands=["ne_bylo"])
async def ne_bylo(message):
    await send_meme(message, memes["ne_bylo"])


@dp.message_handler(commands=["rzaka"])
async def rzaka(message):
    await send_meme(message, memes["rzaka"])


@dp.message_handler(commands=["rzaka_full"])
async def rzaka_full(message):
    await send_meme(message, memes["rzaka_full"])


@dp.message_handler(commands=["rzaka_time"])
async def rzaka_time(message):
    await send_meme(message, memes["rzaka_time"])


@dp.message_handler(commands=["ban"])
async def ban(message):
    msg = message.text.split(maxsplit=1)

    if len(msg) == 1:
        await send_meme(message, "Бан")
    else:
        await send_meme(message, "Бан " + msg[1])


@dp.message_handler(commands=["fake"])
async def polak(message):
    try:
        await message.delete()
    except Exception:
        pass

    try:
        await bot.send_photo(
            message.chat.id, open("media/images/polak.jpg", "rb"),
            reply_to_message_id=message.reply_to_message.message_id
        )
    except AttributeError:
        await message.answer_photo(open("media/images/polak.jpg", "rb"))
