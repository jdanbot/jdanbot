from .bot import dp
from .lib.prettyword import prettyword
from random import choice, randint


@dp.message_handler(commands=["random_ban", "random"])
async def random(message):
    await message.reply(f"Лови бан на {randint(1, 100)} минут")


@dp.message_handler(commands=["random_putin"])
async def random_putin(message):
    await random_person(message, choice(["Обнуленец", "Путин", "Путен"]))


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
        weeks = number / 7

        if number % 7 == 0:
            await message.reply(f'{name} уйдет через {int(weeks)} {prettyword(int(weeks), ["неделя", "недели", "недель"])}')
        else:
            await message.reply(f'{name} уйдет через {int(weeks)} {prettyword(int(weeks), ["неделя", "недели", "недель"])} и {int(number % 7)} {prettyword(int(number % 7), ["день", "дня", "дней"])}')


@dp.message_handler(commands=["da_net"])
async def da_net(message):
    try:
        await message.delete()
    except Exception:
        pass

    await message.reply(choice(["Да", "Нет"]))
