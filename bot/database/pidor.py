import datetime

from .connection import db, manager

from peewee import *


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