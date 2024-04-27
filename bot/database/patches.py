from beanie.operators import Set
from pymongo import ASCENDING, DESCENDING


class BetterDocument:
    @classmethod
    async def get_or_create(cls, data):
        record = await cls.find_one(data)
        if not record:
            record = cls(**data)
            await record.insert()
        return record

    @classmethod
    async def get_or_update(cls, lookup, data):
        record = await cls.find_one(lookup)
        all_data = {**lookup, **data}

        if not record:
            record = cls(**all_data)
            await record.insert()
        else:
            await record.update(Set(data))
        return record

    @classmethod
    async def get_edged(
        cls, lookup=None, default=None, direction=DESCENDING, sort_by="created"
    ):
        umongo_cursor = (
            cls.find(lookup if lookup else {}).sort([(sort_by, direction)]).limit(1)
        )
        async for record in umongo_cursor:
            return record
        return default

    @classmethod
    async def get_latest(cls, lookup=None, default=None):
        return await cls.get_edged(lookup, default, direction=DESCENDING)

    @classmethod
    async def get_earliest(cls, lookup=None, default=None):
        return await cls.get_edged(lookup, default, direction=ASCENDING)
