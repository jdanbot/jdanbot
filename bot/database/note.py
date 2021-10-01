from peewee import CharField, IntegerField, Model
from .connection import db


class Note(Model):
    chatid = IntegerField()
    content = CharField()
    name = CharField()

    class Meta:
        db_table = "notes"
        database = db
        primary_key = False

    def add(chatid, name, text):
        Note.remove(chatid, name)
        Note.create(chatid=chatid, name=name, content=text)

    def get(chatid, name):
        try:
            return (Note.select()
                        .where(Note.chatid == chatid, Note.name == name)
                        .get()).content
        except Exception:
            return None

    def show(chatid):
        notes = Note.select().where(Note.chatid == chatid)
        return [note.name for note in notes]

    def remove(chatid, name):
        return (Note.delete()
                    .where(Note.chatid == chatid, Note.name == name)
                    .execute())
