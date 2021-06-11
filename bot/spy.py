from sqlfocus import SQLTable

from .config import bot, dp, conn, events, command_stats, _
from .lib.text import code, bold, prettyword, fixHTML
from .lib.libtree import make_tree


def _user_counter(users):
    return prettyword(len(users), _("cases.users"))


def _command_counter(users):
    return prettyword(len(users), _("cases.commands"))


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
                    commands=["stats"])
async def calc_stats(message):
    chat_users = await events.select(where=events.chatid == message.chat.id)
    chats_users = await events.select()

    users = []

    for user in chats_users:
        if user[1] not in users:
            users.append(user[1])

    chat_commands = await command_stats.select(where=command_stats.chat_id == message.chat.id)
    chats_commands = await command_stats.select()

    await message.reply(_(
        "spy.users_info",
        local_users=len(chat_users),
        lu_label=_user_counter(chat_users),

        local_commands=len(chat_commands),
        lc_label=_command_counter(chat_commands),


        global_users=len(users),
        gu_label=_user_counter(users),

        global_commands=len(chats_commands),
        gc_label=_command_counter(chats_commands)
    ))
