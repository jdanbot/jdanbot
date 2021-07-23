from peewee import fn, SQL

from .config import bot, dp, Event, CommandStats, _, get_count, manager
from .lib.text import code, bold, prettyword, fixHTML
from .lib.libtree import make_tree


def _user_counter(users):
    return prettyword(users, _("cases.users"))


def _command_counter(users):
    return prettyword(users, _("cases.commands"))


@dp.message_handler(commands=["me"])
async def me_info(message):
    chats = get_count(await manager.execute(
        Event.select(fn.Count(SQL("*")))
             .where(Event.id == message.from_user.id)
    ))
    
    user = await bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    await message.reply(_(
        "spy.about_user",
        name=fixHTML(message.from_user.full_name),
        id=code(message.from_user.id),
        chats=code(chats),
        status=code(user.status)
    ), parse_mode="HTML")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["stats"])
async def calc_stats(message):
    chat_users = get_count(await manager.execute(
        Event.select(fn.Count(SQL("*")))
             .where(Event.chatid == message.chat.id)
    ))

    chats_users = get_count(await manager.execute(
        Event.select(fn.Count(SQL("*")))
    ))

    chat_commands = get_count(await manager.execute(
        CommandStats.select(fn.Count(SQL("*")))
                    .where(CommandStats.chat_id == message.chat.id)
    ))

    chats_commands = get_count(await manager.execute(
        CommandStats.select(fn.Count(SQL("*")))
    ))

    #REWRITE: Пиздецовый стиль сообщенияCommandStats

    await message.reply(_(
        "spy.users_info",
        local_users=chat_users,
        lu_label=_user_counter(chat_users),

        local_commands=chat_commands,
        lc_label=_command_counter(chat_commands),


        global_users=chats_users,
        gu_label=_user_counter(chats_users),

        global_commands=chats_commands,
        gc_label=_command_counter(chats_commands)
    ))
