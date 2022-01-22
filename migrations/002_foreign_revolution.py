"""Peewee migrations -- 002_foreign_revolution.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""


import logging
import sys

from datetime import datetime

sys.path.insert(0, ".")

from bot.config.database import ChatMember, db, Command, Pidor, Poll, Note, Warn
from bot.config import ADMIN_NOTES
from peewee import CharField, IntegerField, Model, DateTimeField

import datetime as dt
import peewee as pw
from decimal import ROUND_HALF_EVEN

from aiogram import types

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


class Event(Model):
    chat_id = IntegerField()
    user_id = IntegerField()
    name = CharField()

    class Meta:
        db_table = "events"
        database = db
        primary_key = False


def chat_member_by_ids(user_id, chat_id) -> ChatMember:
    return ChatMember.get_or_create(user_id=user_id, chat_id=chat_id)[0]


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    migrate_command()
    migrate_pidor()
    migrate_pidor_stats()
    migrate_events()
    migrate_poll()
    migrate_note()
    migrate_warn()


def migrate_command():
    logging.info("Run command table migration")

    db.execute_sql("ALTER TABLE commands RENAME TO commands_old;")
    db.create_tables([Command])

    class CommandOld(Model):
        chat_id = IntegerField()
        user_id = IntegerField()
        command = CharField()

        class Meta:
            db_table = "commands_old"
            database = db
            primary_key = False

    for command_old in CommandOld:
        with db.atomic():
            Command.insert(
                member_id=chat_member_by_ids(
                    user_id=command_old.user_id,
                    chat_id=command_old.chat_id
                ).id,
                command=command_old.command.split("@")[0].lower(),
                params="",
                when_runned=datetime.fromtimestamp(0)
            ).execute()

    db.execute_sql("DROP TABLE commands_old;")


def migrate_pidor():
    logging.info("Run pidor table migration")

    db.execute_sql("ALTER TABLE pidors RENAME TO pidors_old;")
    db.create_tables([Pidor])

    class PidorOld(Model):
        user_id = IntegerField()
        chat_id = IntegerField()
        timestamp = IntegerField()

        class Meta:
            db_table = "pidors_old"
            database = db
            primary_key = False

    for pidor_old in PidorOld:
        with db.atomic():
            member_id = chat_member_by_ids(
                user_id=pidor_old.user_id,
                chat_id=pidor_old.chat_id
            ).id

            pidor = Pidor.insert(
                member_id=member_id,
                is_pidor_allowed=True,
                when_pidor_of_day=datetime.fromtimestamp(pidor_old.timestamp)
            ).execute()

            (ChatMember.update(pidor_id=pidor)
                    .where(ChatMember.id == member_id)
                    .execute())

    db.execute_sql("DROP TABLE pidors_old;")


def migrate_events():
    logging.info("Run events table migration")

    for event in Event:
        message = types.Message(
            chat=types.Chat(
                id=event.chat_id,
                title=None
            )
        )

        message.from_user = types.User(
            id=event.user_id,
            first_name=event.name,
            last_name=None,
            username=None 
        )

        with db.atomic():
            ChatMember.get_by_message(message)

    db.execute_sql("DROP TABLE events;")


def migrate_pidor_stats():
    logging.info("Run pidor_stats table migration")

    class PidorStats(Model):
        user_id = IntegerField()
        chat_id = IntegerField()
        username = CharField()
        count = IntegerField()

        class Meta:
            db_table = "pidor_stats"
            database = db
            primary_key = False

    for stats in PidorStats:
        member_id = chat_member_by_ids(
            user_id=stats.user_id,
            chat_id=stats.chat_id
        )

        Pidor.update(pidor_count=stats.count).where(Pidor.member_id == member_id).execute()

    db.execute_sql("DROP TABLE pidor_stats;")


def migrate_poll():
    logging.info("Run poll table migration")

    db.execute_sql("ALTER TABLE polls RENAME TO polls_old;")
    db.create_tables([Poll])

    class PollOld(Model):
        user_id = IntegerField()
        chat_id = IntegerField()
        poll_id = IntegerField()
        timestamp = IntegerField()
        description = CharField()

        class Meta:
            db_table = "polls_old"
            database = db
            primary_key = False

    for poll_old in PollOld:
        with db.atomic():
            Poll.insert(
                id=poll_old.poll_id,
                author=chat_member_by_ids(
                    user_id=poll_old.user_id,
                    chat_id=poll_old.chat_id
                ).id,
                description=poll_old.description,
                created_at=datetime.fromtimestamp(poll_old.timestamp)
            ).execute()

    db.execute_sql("DROP TABLE polls_old;")


def migrate_note():
    logging.info("Run note table migration")

    db.execute_sql("ALTER TABLE notes RENAME TO notes_old;")
    db.create_tables([Note])

    class NoteOld(Model):
        chat_id = IntegerField()
        content = CharField()
        name = CharField()

        class Meta:
            db_table = "notes_old"
            database = db
            primary_key = False

    for note_old in NoteOld:
        with db.atomic():
            Note.insert(
                name=note_old.name,
                text=note_old.content,
                author=chat_member_by_ids(
                    user_id=0,
                    chat_id=note_old.chat_id
                ).id,
                created_at=datetime.fromtimestamp(0),
                is_admin_note=note_old.name in ADMIN_NOTES
            ).execute()

    db.execute_sql("DROP TABLE notes_old;")


def migrate_warn():
    logging.info("Run warn table migration")

    db.execute_sql("ALTER TABLE warns RENAME TO warns_old;")
    db.create_tables([Warn])

    class WarnOld(Model):
        admin_id = IntegerField()
        user_id = IntegerField()
        chat_id = IntegerField()
        timestamp = IntegerField()
        reason = CharField()

        class Meta:
            db_table = "warns_old"
            database = db
            primary_key = False

    for warn_old in WarnOld:
        with db.atomic():
            Warn.insert(
                who_warned_id=chat_member_by_ids(
                    user_id=warn_old.user_id,
                    chat_id=warn_old.chat_id
                ).id,

                
                who_warn_id=chat_member_by_ids(
                    user_id=warn_old.admin_id,
                    chat_id=warn_old.chat_id
                ).id,
                reason=warn_old.reason,
                warned_at=datetime.fromtimestamp(warn_old.timestamp)
            ).execute()

    db.execute_sql("DROP TABLE warns_old;")


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
