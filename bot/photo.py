from .bot import dp, bot

from .lib.telegram import Telegram
from .lib.photo import Photo
from .lib.html import code, bold

from random import choice


@dp.message_handler(commands=["resize"])
async def resize(message):
    tg = Telegram(bot)

    params = tg.parse(message, 3)

    if params == 404:
        await message.reply("Недостаточное количество параметров: необходимо `3`",
                            parse_mode="Markdown")
        return

    print(params)

    try:
        photo = await tg.photo(message)
    except AttributeError:
        await message.reply("Ответьте на фото")
        return

    file = await bot.download_file(photo[1].file_path)

    with open(f"cache/{photo[0]}.jpg", "wb") as new_file:
        new_file.write(file.read())

    img = Photo(f"cache/{photo[0]}.jpg")

    try:
        img.resize([int(params[1]), int(params[2])])
    except Exception as e:
        await message.reply(f"Произошла ошибка\n{code(e)}",
                            parse_mode="HTML")
        return

    await bot.send_photo(message.chat.id, img.save())
    img.clean()


@dp.message_handler(commands=["text"])
async def text(message):
    tg = Telegram(bot)

    params = message.text.split(" ", maxsplit=4)

    if params == 404:
        await message.reply("Недостаточное количество параметров: необходимо `4`",
                            parse_mode="Markdown")
        return

    print(params)

    try:
        photo = await tg.photo(message)
    except AttributeError:
        await message.reply("Ответьте на фото")
        return

    file = await bot.download_file(photo[1].file_path)

    with open(f"cache/{photo[0]}.jpg", "wb") as new_file:
        new_file.write(file.read())

    img = Photo(f"cache/{photo[0]}.jpg")
    try:
        img.font("fonts/OpenSans-Bold.ttf", int(params[1]))
        img.text(params[2], img.parseXY(params[3]), params[4])
    except Exception as e:
        await message.reply(f"{bold('Произошла ошибка')}\n{code(e)}",
                            parse_mode="HTML")
        return

    await message.reply_photo(img.save())
    img.clean()


@dp.message_handler(commands=["t"])
async def t(message):
    tg = Telegram(bot)

    params = message.text.split(" ", maxsplit=1)

    if params == 404:
        await message.reply("Недостаточное количество параметров: необходимо `2`",
                            parse_mode="Markdown")
        return

    print(params)

    try:
        photo = await tg.photo(message)
    except AttributeError:
        await message.reply("Ответьте на фото")
        return

    file = await bot.download_file(photo[1].file_path)

    with open(f"cache/{photo[0]}.jpg", "wb") as new_file:
        new_file.write(file.read())

    img = Photo(f"cache/{photo[0]}.jpg")
    try:
        img.font("fonts/OpenSans-Bold.ttf", 75)
        img.text("black", (50, 50), params[1])
    except Exception as e:
        await message.reply(f"{bold('Произошла ошибка')}\n{code(e)}",
                            parse_mode="HTML")
        return

    await message.reply_photo(img.save())
    img.clean()


@dp.message_handler(commands=["rectangle"])
async def rectangle(message):
    tg = Telegram(bot)

    params = tg.parse(message, 4)

    if params == 404:
        await message.reply("Недостаточное количество параметров: необходимо `4`",
                            parse_mode="Markdown")
        return

    print(params)

    try:
        photo = await tg.photo(message)
    except AttributeError:
        await message.reply("Ответьте на фото")
        return

    file = await bot.download_file(photo[1].file_path)

    with open(f"cache/{photo[0]}.jpg", "wb") as new_file:
        new_file.write(file.read())

    img = Photo(f"cache/{photo[0]}.jpg")

    try:
        img.rectangle(img.parseXY(params[2]), img.parseXY(params[3]), params[1])
    except Exception as e:
        await message.reply(f"{bold('Произошла ошибка')}\n{code(e)}",
                            parse_mode="HTML")
        return

    await message.reply_photo(img.save())
    img.clean()


@dp.message_handler(commands=["random_color", "color"])
async def random_color(message):
    options = message.text.split(" ", maxsplit=1)
    if len(options) == 1:
        randlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]

        color = ""
        for i in range(0, 6):
            color += str(choice(randlist))

        color = "#" + color

    else:
        if options[1].startswith("#"):
            color = options[1]
        else:
            await message.reply("Вводи цвет в формате hex")
            return

    img = Photo(xy=(200, 200))

    try:
        img.rectangle((0, 0), (200, 200), color)
    except Exception as e:
        await message.reply(f"{bold('Произошла ошибка')}\n{code(e)}",
                            parse_mode="HTML")
        return

    caption = code("#") + bold(color[1:])
    await message.reply_photo(img.save(), caption=caption,
                              parse_mode="HTML")
    img.clean()
