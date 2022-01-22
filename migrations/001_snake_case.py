"""Peewee migrations -- 001_snake_case.py.

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


import peewee as pw

SQL = pw.SQL


class Event(pw.Model):
    chatid = pw.IntegerField()
    userid = pw.IntegerField()
    name = pw.CharField()

    class Meta:
        db_table = "events"


class Note(pw.Model):
    chatid = pw.IntegerField()
    content = pw.CharField()
    name = pw.CharField()

    class Meta:
        db_table = "notes"


class Video(pw.Model):
    channelid = pw.CharField()
    link = pw.CharField()

    class Meta:
        db_table = "videos"


def migrate(migrator, database, fake=False, **kwargs):
    migrator.rename_field(Event, "chatid", "chat_id")
    migrator.rename_field(Event, "id", "user_id")

    migrator.rename_field(Note, "chatid", "chat_id")

    migrator.rename_field(Video, "channelid", "id")
    migrator.rename_field(Video, "link", "links")

    migrator.sql("ALTER TABLE videos RENAME TO feeds;")
    migrator.sql("ALTER TABLE command_stats RENAME TO commands;")
    migrator.sql("ALTER TABLE pidorstats RENAME TO pidor_stats;")


def rollback(migrator, database, fake=False, **kwargs):
    pass
