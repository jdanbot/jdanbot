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
