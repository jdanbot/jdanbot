from beanie.operators import Set
from odmantic import AIOEngine


from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    Awaitable,
    Dict,
    Generator,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import pymongo
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor
from pymongo.database import Database

from odmantic.exceptions import DocumentNotFoundError, DuplicateKeyError
from odmantic.field import FieldProxy, ODMReference
from odmantic.index import ODMBaseIndex
from odmantic.model import Model
from odmantic.query import QueryExpression, SortExpression, and_
from odmantic.session import (
    AIOSession,
    AIOSessionBase,
    AIOTransaction,
    SyncSession,
    SyncSessionBase,
    SyncTransaction,
)
from odmantic.typing import lenient_issubclass

try:
    import motor
    from motor.motor_asyncio import (
        AsyncIOMotorClient,
        AsyncIOMotorClientSession,
        AsyncIOMotorCollection,
        AsyncIOMotorCursor,
        AsyncIOMotorDatabase,
    )
except ImportError:  # pragma: no cover
    motor = None

ModelType = TypeVar("ModelType", bound=Model)


class BetterAIOEngine(AIOEngine):
    async def get_or_create(
        self,
        model: Type[ModelType],
        find_queries: list,
        data: dict
    ):
        record = await self.find_one(model, *find_queries)
        if not record:
            record = model(**data)
            await self.save(record)
        return record

    async def get_or_update(self, *args, **kwargs):
        return await self.get_or_create(*args, **kwargs)

    # @classmethod
    # async def get_edged(
    #     cls, lookup=None, default=None, direction=DESCENDING, sort_by="created"
    # ):
    #     umongo_cursor = (
    #         cls.find(lookup if lookup else {}).sort([(sort_by, direction)]).limit(1)
    #     )
    #     async for record in umongo_cursor:
    #         return record
    #     return default

    # @classmethod
    # async def get_latest(cls, lookup=None, default=None):
    #     return await cls.get_edged(lookup, default, direction=DESCENDING)

    # @classmethod
    # async def get_earliest(cls, lookup=None, default=None):
    #     return await cls.get_edged(lookup, default, direction=ASCENDING)
