from sqlfocus import SQLTable

from .config import bot, dp, conn, events, _
from .lib.text import code, bold, prettyword, fixHTML
from .lib.libtree import make_tree


def _user_counter(users):
    return prettyword(len(users), _("cases.users"))


@dp.message_handler(commands=["me"])
async def me_info(message):
    chats = await events.select(where=events.id == message.from_user.id)
    user = await bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    await message.reply(_(
        "spy.about_user",
        name=fixHTML(message.from_user.full_name),
        id=code(message.from_user.id),
        chats=code(len(chats)),
        status=code(user.status)
    ), parse_mode="HTML")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["users"])
async def calc_users(message):
    chat_users = await events.select(where=events.chatid == message.chat.id)
    chats_users = await events.select()

    users = []

    for user in chats_users:
        if user[1] not in users:
            users.append(user[1])

    await message.reply(_(
        "spy.users_info", 
        local_users=len(chat_users),
        lu_label=_user_counter(chat_users),

        global_users=len(users),
        gu_label=_user_counter(users)
    ))


async def activate_spy(message):
    user = message.from_user
    cur_user = await events.select(where=[
        events.id == user.id,
        events.chatid == message.chat.id
    ])

    if len(cur_user) == 0:
        await events.insert(message.chat.id, user.id, user.full_name)
        await conn.commit()
    else:
        pass
