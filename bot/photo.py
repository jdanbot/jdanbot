from random import choice

from .config import bot, dp, _
from .lib import handlers
from .lib.text import bold, code
from .lib.photo import Photo


@dp.message_handler(commands=["resize"])
@handlers.parse_arguments(4)
@handlers.init_photo_file
async def resize(message, params, img):
    img.resize([int(params[1]), int(params[2])])

    await bot.send_photo(message.chat.id, img.save())


@dp.message_handler(commands=["text"])
@handlers.parse_arguments(5)
@handlers.init_photo_file
async def text(message, params, img):
    img.font("media/fonts/OpenSans-Bold.ttf", int(params[1]))
    img.text(params[2], img.parseXY(params[3]), params[4])

    await message.reply_photo(img.save())


@dp.message_handler(commands=["t"])
@handlers.parse_arguments(2)
@handlers.init_photo_file
async def t(message, params, img):
    img.font("media/fonts/OpenSans-Bold.ttf", 75)
    img.text("black", (50, 50), params[1])

    await message.reply_photo(img.save())


@dp.message_handler(commands=["rectangle"])
@handlers.parse_arguments(4)
@handlers.init_photo_file
async def rectangle(message, params, img):
    img.rectangle(img.parseXY(params[2]),
                  img.parseXY(params[3]),
                  params[1])

    await message.reply_photo(img.save())


@dp.message_handler(commands=["random_color", "color"])
@handlers.parse_arguments(2, without_params=True)
async def random_color(message, params):
    if len(params) == 1:
        randlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                    "A", "B", "C", "D", "E", "F"]

        color = ""
        for _ in range(0, 6):
            color += str(choice(randlist))

        color = "#" + color

    else:
        if params[1].startswith("#"):
            color = params[1]
        else:
            await message.reply(_("errors.hex_only"))
            return

    img = Photo(xy=(200, 200))
    img.rectangle((0, 0), (200, 200), color)

    caption = code("#") + bold(color[1:])
    await message.reply_photo(img.save(), caption=caption,
                              parse_mode="HTML")
