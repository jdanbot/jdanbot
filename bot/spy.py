from sqlfocus import SQLTable

from .config import bot, dp, conn
from .locale import locale
from .lib.text import code, prettyword


def _user_counter(users):
    return prettyword(len(users), locale.users)


@dp.message_handler(commands=["me"])
async def me_info(message):
    msg_template = (
        "*Full name:* {name}\n" +
        "*ID:* `{id}`\n\n" +
        "*Common chats*: `{chats}`\n" +
        "*User status*: {status}"
    )

    table = SQLTable("events", conn)
    chats = await table.select(where=[f"id={message.from_user.id}"])

    user = await bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    await message.reply(msg_template.format(
        name=message.from_user.full_name,
        id=message.from_user.id,
        chats=len(chats),
        status=user.status
    ), parse_mode="Markdown")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["users"])
async def calc_users(message):
    users = []
    table = SQLTable("events", conn)

    chat_users = await table.selectall(where=[f"chatid={message.chat.id}"])
    e = await table.select()

    for user in e:
        if user[1] in users:
            pass
        else:
            users.append(user[1])

    # В этом чяте <num> пользователей
    # Всего <num> пользователей

    text = "В этом чяте {} {}\nВсего {} {}"

    await message.reply(text.format(len(chat_users), _user_counter(chat_users),
                                    len(users), _user_counter(users)))


async def activate_spy(message):
    table = SQLTable("events", conn)
    user = message.from_user

    events = await table.select(where=[
        f"id={message.from_user.id}",
        f"chatid={message.chat.id}"
    ])

    if len(events) == 0:
        table.insert(message.chat.id, user.id, user.full_name)
        await conn.commit()
    else:
        pass
