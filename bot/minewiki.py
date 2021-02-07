from .config import bot, dp
from .lib.html import code
from .lib.lurkmore import Lurkmore

mine = Lurkmore()
mine.url = "https://minecraft-ru.gamepedia.com/api.php"
mine.url2 = "https://minecraft-ru.gamepedia.com"


@dp.message_handler(commands=["mine", "minewiki"])
async def getmine(message):
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        await message.reply("Напишите название статьи")
        return

    name = options[1]
    print(f"[minewiki] {name}")

    s = await mine.opensearch(name)

    if len(s) == 0:
        await message.reply("Не найдено")
        return

    p = await mine.getPage(s[0])
    i = await mine.getImagesList(s[0])

    if len(i) != 0:
        try:
            image = await mine.getImage(i[0])
            image = image[6:-1]

            await bot.send_chat_action(message.chat.id, "upload_photo")
            await message.reply_photo(image, caption=mine.parse(p)[:1000],
                                      parse_mode="HTML")
        except Exception as e:
            await bot.send_chat_action(message.chat.id, "typing")
            await message.reply(code(e), parse_mode="HTML")
            try:
                await message.reply(mine.parse(p)[:4096], parse_mode="HTML")
            except Exception:
                await message.reply(mine.parse(p)[:4096])
    else:
        await message.reply(mine.parse(p)[:4096], parse_mode="HTML")
