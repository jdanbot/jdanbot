from .bot import bot, dp
from .lib.html import code
from .lib.lurkmore import Lurkmore

lurk = Lurkmore()


@dp.message_handler(commands=["lurk"])
async def getlurk(message):
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        await message.reply("Напишите название статьи")
        return

    name = options[1]
    print(f"[Lurkmore] {name}")

    s = await lurk.opensearch(name)

    if len(s) == 0:
        await message.reply("Не найдено")
        return

    p = await lurk.getPage(s[0])
    i = await lurk.getImagesList(s[0])

    if len(i) != 0:
        try:
            image = await lurk.getImage(i[0])
            await bot.send_chat_action(message.chat.id, "upload_photo")
            await message.reply_photo(image, caption=lurk.parse(p)[:1000],
                                      parse_mode="HTML")
        except Exception as e:
            await bot.send_chat_action(message.chat.id, "typing")
            await message.reply(code(e), parse_mode="HTML")
            try:
                await message.reply(lurk.parse(p)[:4096], parse_mode="HTML")
            except Exception:
                await message.reply(lurk.parse(p)[:4096])
    else:
        await message.reply(lurk.parse(p)[:4096], parse_mode="HTML")
