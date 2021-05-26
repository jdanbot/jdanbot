from ..config import dp, bot, _
from ..lib.lurkmore import Lurkmore
from ..lib.text import code

import aiogram


@dp.message_handler(commands=["railgun"])
async def railgun(message):
    await fandom(message, "Railgun",
                 "https://toarumajutsunoindex.fandom.com/api.php")


@dp.message_handler(commands=["fallout"])
async def fallout(message):
    await fandom(message, "Fallout", "https://fallout.fandom.com/ru/api.php")


@dp.message_handler(commands=["kaiser", "kaiserreich"])
async def kaiser(message):
    await fandom(message, "Kaiserreich", "https://kaiserreich.fandom.com/ru/api.php")


@dp.message_handler(commands=["doom"])
async def doom(message):
    await fandom(message, "DooM", "https://doom.fandom.com/api.php")


async def fandom(message, fname, url):
    f = Lurkmore()
    f.url = url
    f.url2 = url.replace("api.php", "")

    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        await message.reply(_("errors.enter_wiki_query").format(options[0]),
                            parse_mode="Markdown")
        return

    name = options[1]
    print(f"[Fandom: {fname}] {name}")

    s = await f.opensearch(name)

    if len(s[1]) == 0:
        await message.reply(_("error.not_found")) 
        return

    p = await f.getPage(s[1][0])
    i = f.getImageFromFandomPage(p)
    url = s[-1][0]

    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton(text=_("wiki.read_full"),
                                                    url=url))

    if i != 404:
        try:
            # Send page in normal mode
            await bot.send_chat_action(message.chat.id, "upload_photo")
            await message.reply_photo(i, caption=f.parse(p)[:1000],
                                      parse_mode="HTML", reply_markup=keyboard)
        except Exception as e:
            # Send error message
            await bot.send_chat_action(message.chat.id, "typing")
            await message.reply(code(e), parse_mode="HTML")

            try:
                # Try send only html
                await message.reply(f.parse(p)[:4096], reply_markup=keyboard,
                                    parse_mode="HTML")
            except Exception:
                # Try send only text
                await message.reply(f.parse(p)[:4096], reply_markup=keyboard)
    else:
        parsed_text = f.parse(p)[:4096]
        try:
            # Send html in normal mode
            await message.reply(parsed_text, reply_markup=keyboard,
                                parse_mode="HTML")
        except Exception:
            # Try send text
            await message.reply(parsed_text, reply_markup=keyboard)
