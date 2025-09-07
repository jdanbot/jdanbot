from typing import Any, override

from pydantic.config import ConfigDict
from tortoise import Model as Table
from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.contrib.pydantic.creator import (
    pydantic_model_creator,
)


class BaseTable(Table):
    @override
    class Meta:
        abstract: bool = True

    @property
    def model(self) -> type[PydanticModel]:
        return pydantic_model_creator(
            self.__class__,
            model_config=ConfigDict(
                arbitrary_types_allowed=True,
                extra="forbid",
                validate_assignment=True,
            ),
        )

    def __rich_repr__(self) -> PydanticModel:
        return self.model(
            **dict(
                filter(
                    lambda item: not item[0].startswith("_"),
                    self.__dict__.items(),
                )
            )
        )

    @classmethod
    async def count(cls) -> int:
        return await cls.filter().count()

    async def update(self, data: dict[Any, Any] | None = None, **kwargs):
        if data is None:
            data: dict[Any, Any] = {}

        self.update_from_dict(data=data or kwargs)

        return await self.save()
