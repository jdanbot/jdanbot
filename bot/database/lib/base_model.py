from tortoise import Model


class BaseModel(Model):
    @classmethod
    async def count(cls) -> int:
        return await cls.filter().count()

    async def update(self, data: dict = None, **kwargs):
        if data is None:
            data = {}

        self.update_from_dict(data=data | kwargs)

        return await self.save()

    class Meta:
        abstract = True
