from typing import Self

from piccolo.table import Table


class BetterTable(Table):
    @classmethod
    async def get(cls, id: int) -> Self:
        return (await cls.select().where(cls.id == id))[0]

    @classmethod
    async def get_or_none(cls, id: int) -> Self:
        return (
            res[0]
            if len(res := await cls.select().where(cls.id == id)) == 1
            else None
        )

    @classmethod
    async def get_or_update(cls, id, defaults) -> Self:
        await cls.objects().get_or_create(
            cls.id == id,
            defaults=defaults
        )

        await cls.update(defaults).where(cls.id == id)
        return await cls.get(id)