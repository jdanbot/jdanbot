from .telegram import (
    Chat,
    User,
    Member,
)
from .command import Command
import asyncio

from .engine import engine

from pprint import pprint


async def run_db():
    members = await engine.find_one(
        Member,
        {"tg_id": {"$regex": "@-100500$"}}
    )

    pprint(members)

    print("Hallo, Welt!")


if __name__ == "__main__":
    asyncio.run(run_db())
