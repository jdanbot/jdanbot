from .bot import bot, dp
from .lib.html import code
from .lib.lurkmore import Lurkmore

# from tghtml import tghtml

lurk = Lurkmore()


@dp.message_handler(commands=["lurk"])
async def L(message):
    await getOldWiki(message)


@dp.message_handler(commands=["absurd"])
async def absurd(message):
    await getOldWiki(message, "Absurdopedia",
                     "https://absurdopedia.net/w/api.php",
                     "https://absurdopedia.net/wiki/")


@dp.message_handler(commands=["archwiki"])
async def archwiki(message):
    await getOldWiki(message, "archwiki",
                     "https://wiki.archlinux.org/api.php",
                     "https://wiki.archlinux.org")


async def getOldWiki(message, n="Lurkmore",
                     url="https://ipv6.lurkmo.re/api.php",
                     url2="https://ipv6.lurkmo.re"):
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        await message.reply("Напишите название статьи")
        return

    lurk.url = url
    lurk.url2 = url2

    name = options[1]
    print(f"[{n}] {name}")

    s = await lurk.opensearch(name)

    if len(s[1]) == 0:
        s = await lurk.search(name)

        if len(s) == 0:
            await message.reply("Не найдено")
            return
    else:
        s = s[1]

    p = await lurk.getPage(s[0])
    i = await lurk.getImagesList(s[0])



    arch_class = "archwiki-template-meta-related-articles-start"
    tagBlocklist = [
        ["table", {"class": "lm-plashka"}],
        ["table", {"class": "lm-plashka-tiny"}],
        ["table", {"class": "tpl-quote-tiny"}],
        ["div", {"class": "thumbinner"}],
        ["div", {"class": "gallerytext"}],
        ["aside"],
        ["table"],
        ["div", {"class": arch_class}],
        ["div", {"class": "noprint"}]
    ]

    parsed_text = lurk.parse(p)[:4096]

    if len(i) != 0:
        try:
            # Send page in normal mode
            image = await lurk.getImage(i[0])
            await bot.send_chat_action(message.chat.id, "upload_photo")
            await message.reply_photo(image, caption=parsed_text[:1000],
                                      parse_mode="HTML")
        except Exception as e:
            # Send error message
            await bot.send_chat_action(message.chat.id, "typing")
            await message.reply(code(e),
                                parse_mode="HTML")

            try:
                # Try send only html
                await message.reply(parsed_text,
                                    parse_mode="HTML")
            except Exception:
                # Try send only text
                await message.reply(parsed_text)
    else:
        try:
            # Send html in normal mode
            await message.reply(parsed_text,
                                parse_mode="HTML")
        except Exception:
            # Try send text
            await message.reply(parsed_text)
