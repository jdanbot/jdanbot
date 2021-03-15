from ..lib.text import prettyword
from ..locale import locale
from ..config import dp

from random import choice, randint


@dp.message_handler(commands=["random_ban", "random"])
async def random(message):
    await message.reply(f"Лови бан на {randint(1, 100)} минут")


@dp.message_handler(commands=["random_putin"])
async def random_putin(message):
    await random_person(message, choice(["Обнуленец", "Путин", "Краб"]))


@dp.message_handler(commands=["random_lukash", "luk", "lukash"])
async def random_lukash(message):
    await random_person(message, choice(["Лукашенко", "Лукашеску", "3%",
                                         "Саша", "Саня"]))


async def random_person(message, name):
    number = randint(0, 500)

    if number == 1:
        await message.reply("Иди нахуй))")
        return

    else:
        weeks_num = round(number / 7)
        days_num = round((number - weeks_num) % 7)

        if weeks_num == 0:
            await message.reply(f'{name} уйдет сегодня')

        elif days_num == 0:
            date = prettyword(int(weeks_num), locale.weeks)
            await message.reply(f'{name} уйдет через {int(weeks_num)} {date}')

        else:
            weeks = prettyword(int(weeks_num), locale.weeks)
            days = prettyword(int(days_num), locale.days)

            date = "{} {} и {} {}".format(weeks_num, weeks,
                                          days_num, days)

            await message.reply(f'{name} уйдет через {date}')


@dp.message_handler(commands=["da_net"])
async def da_net(message):
    try:
        await message.delete()
    except Exception:
        pass

    await message.reply(choice(["Да", "Нет"]))
