from typing import Any, override

from tortoise import Model as Table


class BaseTable(Table):
    @override
    class Meta:
        abstract: bool = True

    def __rich_repr__(self):
        for field_name in self._meta.fields:
            value = getattr(self, field_name)

            yield field_name, value

    @classmethod
    async def count(cls) -> int:
        return await cls.filter().count()

    async def update(
        self, data: dict[Any, Any] | None = None, **kwargs
    ):
        if data is None:
            data: dict[Any, Any] = {}

        self.update_from_dict(data=data or kwargs)

        return await self.save()
