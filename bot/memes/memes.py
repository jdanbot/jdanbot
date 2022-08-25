from ..config import dp
from aiogram import types


async def send_meme(
    message: types.Message,
    text: str,
    is_sticker: bool = False
):
    reply = message.reply_to_message

    if is_sticker:
        reply.reply = reply.reply_sticker
        message.answer = message.answer_sticker

    try:
        await reply.reply(text)
    except AttributeError:
        await message.answer(text)

    try:
        await message.delete()
    except Exception:
        pass


memes = {
    "bylo": "Было",
    "ne_bylo": "Не было",
    "rzaka": "РЖАКА-СМЕЯКА 🤣🤣🤣🤣😋😋😋😋😋😋СРАЗУ ВИДНО РУССКОГО ЧЕЛОВЕКА😃😃😃😃😃🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺👍👍👍👍ТУПЫЕ ПЕНДОСЫ В СВОЕЙ ОМЕРИКЕ ДО ТАКОГО БЫ НЕ ДОДУМАЛИСЬ😡😡😡😡😡😡👎👎👎👎👎🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸",  # noqa
    "rzaka_full": "РЖАКА-СМЕЯКА 🤣🤣🤣🤣😋😋😋😋😋😋СРАЗУ ВИДНО РУССКОГО ЧЕЛОВЕКА😃😃😃😃😃🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺👍👍👍👍ТУПЫЕ ПЕНДОСЫ В СВОЕЙ ОМЕРИКЕ ДО ТАКОГО БЫ НЕ ДОДУМАЛИСЬ😡😡😡😡😡😡👎👎👎👎👎🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸РОССИЯ ВПЕРЕД😊😊😊😊😊😊😃😃😃😃😃😃😋😋😋😋🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺АХАХАХАХАХ😃😃😃😃😃СМЕШНО ПОШУТИЛ ЧУВАЧОК👉👋👍👍👍👍👍ТАКОЕ МОЖНО УВИДЕТЬ ТОЛЬКО В РОССИИ ✌️✌️😲😲😲 ХААХАХА ВОТ УМОРА🤣🤣🤣🤣АЖ АМЕРИКА ВЗОРВАЛАСЬ ОТ СМЕХА😜😜😜😜😜😜😜ВСЯ ЕВРОПА В ШОКЕ🤙🤙🤙🤙🤙🤙🤙АХХАХАХАХА БЛИН НЕ МОГУ ОСТАНОВИТЬСЯ СМЕЮСЬ КАТАЮСЬ ПО ПОЛУ😬😬😬😵😵😵😵😵ВОТ ЭТО ШУТКА РЖАКА СМЕЯЛИСЬ ВСЕЙ МАРШРУТКОЙ РЖАЛА 848393938347292929647492918363739304964682010 ЧАСОВ РЖОМБА ПРЯМА НЕРЕАЛЬНАЯ РЖАКА ШУТКА 😂😂😂😂😂😂😂😂🤔😂😂😹😹😹😹😹😹😹😹😹😂😂😂😂👍👍👍👍👍👍👍👍👍👍АХАХА , КАК СМЕШНО !!!!! Я НЕ МОГУ, ПОМОГИТЕ , ЗАДЫХАЮСЬ ОТ СМЕХА 😂🤣🤣😄🤣😂🤣🤣🤣 СПАСИБО , ВЫ СДЕЛАЛИ МОЙ ДЕНЬ !!! КАК ЖЕ ОРИГИНАЛЬНО !!! Я В ВОСТОРГЕ!!!!!!😀😃😀😃🤣😁🤣🤣🤣🤣🤣😀🤣😀😀🤣🤣😀🤣😀🤣😀🤣😀🤣😀🤣😀😀🤣😀🤣😁🤣😁🤣😁🤣😁😁🤣😁",  # noqa
    "rzaka_time": 848393938347292929647492918363739304964682010
}
stickers = {
    "pizda": "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ",  # noqa
    "net_pizdy": "CAACAgIAAx0CUDyGjwACAQ1fCFkcDHIDN_h0qHDu7LgvS8SBIgAC4AADlJlpL8ZF00AlPORXGgQ",  # noqa
    "pizda_tebe": "CAACAgIAAxkBAAILHV9qcv047Lzwp_B64lDlhtOD-2RGAAIgAgAClJlpL5VCBwPTI85YGwQ",  # noqa
    "xui": "CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ",  # noqa
    "net_xua": "CAACAgIAAx0CUDyGjwACAQ9fCFkfgfI9pH9Hr96q7dH0biVjEwAC4gADlJlpL_foG56vPzRPGgQ"  # noqa
}


@dp.message_handler(commands=memes.keys())
async def bylo(message: types.Message):
    await send_meme(
        message,
        memes[message.get_command(pure=True)]
    )


@dp.message_handler(commands=stickers.keys())
async def meme_stickers(message: types.Message):
    await send_meme(
        message,
        stickers[message.get_command(pure=True)],
        is_sticker=True
    )


@dp.message_handler(commands=["ban"])
async def ban(message):
    msg = message.text.split(maxsplit=1)
    await send_meme(message, "Бан " + (msg[1] if len(msg) > 1 else ""))
