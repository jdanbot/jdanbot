"""Peewee migrations -- 003_pidor_events.py.

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


sys.path.insert(0, ".")

from bot.schemas import db, Pidor, PidorEvent
from peewee import IntegerField, Model, DateTimeField, BooleanField

import peewee as pw

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    migrate_pidor()


def migrate_pidor():
    logging.info("Run pidor table migration")

    db.execute_sql("ALTER TABLE pidors RENAME TO pidors_old;")
    db.create_tables([Pidor, PidorEvent])

    class PidorOld(Model):
        member_id = IntegerField()
        pidor_count = IntegerField(default=0)
        is_pidor_allowed = BooleanField(default=True)
        when_pidor_of_day = DateTimeField(null=True)

        class Meta:
            db_table = "pidors_old"
            database = db

    with db.atomic():
        for pidor_old in PidorOld:
            match pidor_old.pidor_count:
                case 0:
                    pidor_event = None
                case 1:
                    pidor_event = PidorEvent.insert(
                        pidor_id=pidor_old.id,
                        caused_at=pidor_old.when_pidor_of_day
                    ).execute()
                case _:
                    for __ in range(0, pidor_old.pidor_count - 1):
                        PidorEvent.insert(
                            pidor_id=pidor_old.id,
                            caused_at=None
                        ).execute()

                    pidor_event = PidorEvent.insert(
                        pidor_id=pidor_old.id,
                        caused_at=pidor_old.when_pidor_of_day
                    ).execute()

            Pidor.insert(
                member_id=pidor_old.member_id,
                is_pidor_allowed=pidor_old.member_id,
                latest_pidor_event=pidor_event
            ).execute()

    db.execute_sql("DROP TABLE pidors_old;")


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
