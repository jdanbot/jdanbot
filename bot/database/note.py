from datetime import datetime
from typing import Optional

from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField, Model

from .chat import Chat
from .chat_member import ChatMember
from .connection import db



class Note(Model):
    name = CharField()
    text = CharField()

    is_admin_note = BooleanField()

    author = ForeignKeyField(ChatMember, column_name="author_id")
    created_at = DateTimeField(default=datetime.now)

    editor = ForeignKeyField(ChatMember, column_name="editor_id",  null=True)
    edited_at = DateTimeField(null=True)

    class Meta:
        db_table = "notes"
        database = db

    def find_note(chat_id: int, query: str) -> "Note":
        return (Note.select()
                    .join(ChatMember, on=Note.author_id == ChatMember.id)
                    .join(Chat, on=ChatMember.chat_id == Chat.id)
                    .where(Chat.id == chat_id, Note.name == query))

    async def add(member: ChatMember, name: str, text: str, is_admin_note: bool) -> bool:
        if is_admin_note and not await member.check_admin():
            raise AttributeError

        results = Note.find_note(member.chat.id, name)
        is_edit = len(results) > 0

        if not is_edit:
            Note.create(
                name=name,
                text=text,
                author_id=member.id,
                is_admin_note=is_admin_note
            )
        else:
            Note.update(
                editor=member,
                edited_at=datetime.now(),
                text=text
            ).where(Note.id == results[0].id).execute()

        return is_edit

    def get(chat_id: int, name: str) -> Optional[str]:
        try:
            return list(
                Note.select()
                    .join(ChatMember, on=Note.author_id == ChatMember.id)
                    .join(Chat, on=ChatMember.chat_id == Chat.id)
                    .where(Chat.id == chat_id, Note.name == name)
            )[0].text
        except Exception as e:
            return None

    def show(chat_id: int) -> list[str]:
        notes = (
            Note.select()
                .join(ChatMember, on=Note.author == ChatMember.id)
                .join(Chat, on=ChatMember.chat_id == Chat.id)
                .where(Chat.id == chat_id))

        return [note.name for note in notes]

    async def remove(member: ChatMember, name: str):
        note = (
            Note.select()
                .join(ChatMember, on=Note.author_id == ChatMember.id)
                .join(Chat, on=ChatMember.chat_id == Chat.id)
                .where(Chat.id == member.chat.id, Note.name == name)
        )[0]

        if note.is_admin_note and not await member.check_admin():
            raise AttributeError

        return Note.delete().where(Note.id == note.id).execute()
