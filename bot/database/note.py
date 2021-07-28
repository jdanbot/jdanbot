from peewee import *
from .connection import db, manager


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