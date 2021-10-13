from peewee import CharField, IntegerField, Model
from .connection import db


class Note(Model):
    chat_id = IntegerField()
    content = CharField()
    name = CharField()

    class Meta:
        db_table = "notes"
        database = db
        primary_key = False

    def add(chat_id, name, text):
        Note.remove(chat_id, name)
        Note.create(chat_id=chat_id, name=name, content=text)

    def get(chat_id, name):
        try:
            return (Note.select()
                        .where(Note.chat_id == chat_id, Note.name == name)
                        .get()).content
        except Exception:
            return None

    def show(chat_id):
        notes = Note.select().where(Note.chat_id == chat_id)
        return [note.name for note in notes]

    def remove(chat_id, name):
        return (Note.delete()
                    .where(Note.chat_id == chat_id, Note.name == name)
                    .execute())
