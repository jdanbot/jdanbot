import datetime

from .connection import db

from peewee import IntegerField, Model


class Pidor(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    timestamp = IntegerField()

    class Meta:
        db_table = "pidors"
        database = db
        primary_key = False

    async def getPidorInfo(
        chat_id: int,
        period: datetime.timedelta = datetime.timedelta(hours=24)
    ) -> list["Pidor"]:
        period_bound = int((datetime.datetime.now() - period).timestamp())

        return list(Pidor.select()
                         .where(Pidor.timestamp >= period_bound,
                                Pidor.chat_id == chat_id))
