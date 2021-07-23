from aiogram.utils import exceptions

import asyncio
import json
import datetime

from .config import DB_PATH
from .bot import bot

from peewee import *
from peewee_async import Manager

from .lib.async_sqlite import SqliteDatabase, onefor, get_count


db = SqliteDatabase(DB_PATH)


class Video(Model):
    channelid = CharField()
    link = CharField()

    class Meta:
        db_table = "videos"
        database = db
        primary_key = False

    async def save(channelid, link):
        links = list(await manager.execute(
            Video.select()
                 .where(Video.channelid == channelid)
        ))

        if len(links) > 0:
            links = json.loads(links[0].link)[-15:]
            links.append(link)

            links_str = json.dumps(links)

            await manager.execute(
                Video.update(link=links_str)
                     .where(Video.channelid == channelid)
            )

        else:
            links = [link]
            links_str = json.dumps(links)

            await manager.execute(
                Video.insert(channelid=channelid,
                             link=links_str)
            )


class Warn(Model):
    admin_id = IntegerField()
    user_id = IntegerField()
    chat_id = IntegerField()
    timestamp = IntegerField()
    reason = CharField()

    class Meta:
        db_table = "warns"
        database = db
        primary_key = False

    async def count_wtbans(user_id, chat_id,
                           period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())

        return get_count(await manager.execute(
            Warn.select(fn.Count(SQL("*")))
                .where(
                    Warn.timestamp >= period_bound,
                    Warn.user_id == user_id,
                    Warn.chat_id == chat_id
                )
        ))

    async def mark_chat_member(user_id, chat_id, admin_id, reason):
        await manager.execute(
            Warn.insert(user_id=user_id, admin_id=admin_id,
                        chat_id=chat_id, reason=reason,
                        timestamp=int(datetime.datetime.now().timestamp()))
        )


class Pidor(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    timestamp = IntegerField()

    class Meta:
        db_table = "pidors"
        database = db
        primary_key = False

    async def getPidorInfo(chat_id, period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())

        return list(await manager.execute(
            Pidor.select()
                 .where(Pidor.timestamp >= period_bound,
                        Pidor.chat_id == chat_id)
        ))


class PidorStats(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    username = CharField()
    count = IntegerField()

    class Meta:
        db_table = "pidorstats"
        database = db
        primary_key = False


class Poll(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    poll_id = IntegerField()
    timestamp = IntegerField()
    description = CharField()

    class Meta:
        db_table = "polls"
        database = db
        primary_key = False

    async def add(user_id, chat_id,
                  poll_id, description):
        now = datetime.datetime.now()
        period = int(now.timestamp())

        await manager.execute(
            Poll.insert(chat_id=chat_id, user_id=user_id,
                        poll_id=poll_id, description=description,
                        timestamp=period)
        )

    async def close_old():
        period = datetime.timedelta(hours=24)
        now = datetime.datetime.now()
        period_bound = int((now - period).timestamp())

        polls = await manager.execute(
            Poll.select()
                .where(Poll.timestamp <= period_bound)
        )

        for poll in polls:
            try:
                poll_res = await bot.stop_poll(poll.chat_id,
                                               poll.poll_id)

            except (exceptions.PollHasAlreadyBeenClosed,
                    exceptions.MessageWithPollNotFound):
                await manager.execute(
                    Poll.delete()
                        .where(Poll.timestamp <= period_bound,
                               Poll.chat_id == poll.chat_id,
                               Poll.poll_id == poll.poll_id)
                )

                continue

            if poll_res.is_closed:
                await manager.execute(
                    Poll.delete()
                        .where(Poll.timestamp <= period_bound)
                )

            else:
                await bot.stop_poll(poll.chat_id, poll.poll_id)


class Note(Model):
    chatid = IntegerField()
    content = CharField()
    name = CharField()

    class Meta:
        db_table = "notes"
        database = db
        primary_key = False

    async def add(chatid, name, text):
        await Note.remove(chatid, name)

        return await manager.execute(
            Note.insert(chatid=chatid, name=name, content=text)
        )

    async def get(chatid, name):
        note = list(await manager.execute(
            Note.select()
                .where(Note.chatid == chatid, Note.name == name)
        ))

        if len(note) > 0:
            return note[0].content

    async def show(chatid):
        notes = await manager.execute(
            Note.select()
                .where(Note.chatid == chatid)
        )

        return [note.name for note in notes]

    async def remove(chatid, name):
        return await manager.execute(
            Note.delete()
                .where(Note.chatid == chatid, Note.name == name)
        )


class CommandStats(Model):
    chat_id = IntegerField()
    user_id = IntegerField()
    command = CharField()

    class Meta:
        db_table = "command_stats"
        database = db
        primary_key = False


class Event(Model):
    chatid = IntegerField()
    id = IntegerField()
    name = CharField()

    class Meta:
        db_table = "events"
        database = db
        primary_key = False

    async def reg_user_in_db(message):
        user = message.from_user

        cur_user = list(await manager.execute(
            Event.select()
                 .where(Event.id == user.id,
                        Event.chatid == message.chat.id)
        ))

        if len(cur_user) == 0:
            await manager.execute(
                Event.insert(
                    chatid=message.chat.id,
                    id=user.id,
                    name=user.full_name
                )
            )


for model in (Note, Event, CommandStats, Warn, Poll, Video,
              Pidor, PidorStats):
    model.create_table(True)

manager = Manager(db)

db.close()
db.set_allow_sync(False)