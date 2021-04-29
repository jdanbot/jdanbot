import aiosqlite
from aiogram.utils import exceptions
from sqlfocus import SQLTableBase, SQLTable
from sqlfocus.helpers import sstr

import asyncio
import json
import datetime

from .config import DB_PATH
from .bot import bot


async def connect_db():
    return await aiosqlite.connect(DB_PATH)


class Videos(SQLTableBase):
    async def save(self, channelid, link):
        links = await self.select(where=f"{channelid = }")

        try:
            links = json.loads(links[0][1])[-15:]
            links.append(link)
        except IndexError:
            links = [link]

        links_str = json.dumps(links)

        await self.delete(where=f"{channelid = }")
        await self.insert(channelid, links_str)

        await self.conn.commit()


class Warns(SQLTableBase):
    async def count_wtbans(self, user_id, chat_id,
                           period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())
        w = await self.select(where=[
            self.timestamp >= period_bound,
            f"{user_id = }", f"{chat_id = }"
        ])

        return len(w)

    async def mark_chat_member(self, user_id, chat_id, admin_id, reason):
        await self.insert(user_id, admin_id, chat_id,
                          int(datetime.datetime.now().timestamp()), sstr(reason))

        await conn.commit()


class Pidors(SQLTableBase):
    async def getPidorInfo(self, chat_id,
                           period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())
        return await self.select(where=[
            self.timestamp >= period_bound, f"{chat_id = }"
        ])


class Polls(SQLTableBase):
    async def add_poll(self, user_id, chat_id,
                       poll_id, description):
        now = datetime.datetime.now()
        period = int(now.timestamp())

        return await self.insert(chat_id, user_id, poll_id,
                                 description, period)


    async def close_old(self):
        period = datetime.timedelta(hours=24)
        now = datetime.datetime.now()
        period_bound = int((now - period).timestamp())

        where = self.timestamp <= period_bound
        polls = await self.select(where=where)

        for poll in polls:
            try:
                poll_res = await bot.stop_poll(poll[0], poll[2])

            except (exceptions.PollHasAlreadyBeenClosed,
                    exceptions.MessageWithPollNotFound):
                await self.delete(where=[
                    where,
                    f"chat_id = {poll[0]}",
                    f"poll_id = {poll[2]}"
                ])
                continue

            if poll_res.is_closed:
                await self.delete(where=where)
            else:
                await bot.stop_poll(poll[0], poll[2])


conn = asyncio.run(connect_db())

events = SQLTable("events", conn)
videos = Videos(conn)
warns = Warns(conn)
notes = SQLTable("notes", conn)
pidors = Pidors(conn)
pidorstats = SQLTable("pidorstats", conn)
polls = Polls(conn)


async def init_db():
    await events.create(exists=True, schema=(
        ("chatid", "INTEGER"),
        ("id", "INTEGER"),
        ("name", "TEXT")
    ))

    await videos.create(exists=True, schema=(
        ("channelid", "TEXT"),
        ("links", "TEXT")
    ))

    await warns.create(exists=True, schema=(
        ("user_id", "INTEGER"),
        ("admin_id", "INTEGER"),
        ("chat_id", "INTEGER"),
        ("timestamp", "INTEGER"),
        ("reason", "TEXT")
    ))

    await notes.create(exists=True, schema=(
        ("chatid", "INTEGER"),
        ("name", "TEXT"),
        ("content", "TEXT")
    ))

    await pidors.create(exists=True, schema=(
        ("chat_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("timestamp", "INTEGER")
    ))

    await pidorstats.create(exists=True, schema=(
        ("chat_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("username", "TEXT"),
        ("count", "INTEGER")
    ))

    await polls.create(exists=True, schema=(
        ("chat_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("poll_id", "INTEGER"),
        ("description", "TEXT"),
        ("timestamp", "INTEGER")
    ))

asyncio.run(init_db())
