# please use late mongodb tree code

import asyncio
import sys

sys.path.append(".")

from bot.schemas import ChatMember, Command as CommandOld, ChatMember, Chat as ChatOld
from bot.database import Member, Command, Chat, run_db

from beanie.operators import Push

import pendulum as pdl


async def migrate():
    await run_db()

    print("Hallo, Welt!")
    await migrate_members()
    # await migrate_commands()
    # await migrate_chat()


async def migrate_members():
    for chat_member in ChatMember.select():
        print(chat_member.id)
        print(chat_member.chat_id)

        if chat_member.chat_id > 0:
            continue

        try:
            chat_member.chat
        except:
            continue

        chat = await Chat.find_one(Chat.tg_id == chat_member.chat_id)

        try:
            await chat.update(Push({
                Chat.members: Member(
                    id=f"{chat_member.user_id}@{chat_member.chat_id}",
                    username=chat_member.user.username,
                    first_name=chat_member.user.first_name,
                    last_name=chat_member.user.last_name
                )
            }))
            print("true!")
        except:
            pass


async def migrate_chat():
    await Chat.insert_many([
        Chat(
            tg_id=cht.id,
            username=cht.username,
            title=cht.title
        ) for cht in ChatOld.select()
    ])


async def migrate_commands():
    await Command.insert_many([
        Command(
            user_id=(member := ChatMember.get(cmd.member_id)).user_id,
            chat_id=member.chat_id,
            name=cmd.command,
            params=cmd.params,
            runned_at=pdl.parse(str(cmd.when_runned))
        ) for cmd in CommandOld.select()
    ])

    for command in CommandOld.select():
        print(command.command)


if __name__ == "__main__":
    asyncio.run(migrate())
