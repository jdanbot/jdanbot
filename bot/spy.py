from sqlfocus import SQLTable

from .config import bot, dp, conn, events, _
from .lib.text import code, prettyword


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
        name=message.from_user.full_name,
        id=message.from_user.id,
        chats=len(chats),
        status=user.status
    ), parse_mode="Markdown")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["users"])
async def calc_users(message):
    chat_users = await events.select(where=events.chatid == message.chat.id)
    chats_users = await events.select()

    users = []
    users = [user[1] for user in chats_users if user[1] not in users]

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

    if len(cur_users) == 0:
        await events.insert(message.chat.id, user.id, user.full_name)
        await conn.commit()
    else:
        pass
