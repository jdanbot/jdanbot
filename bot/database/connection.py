from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from .telegram import PidorEvent, PidorEvents, Pidor, Chat, User, Member
from .command import Command
import asyncio

from pprint import pprint


client = AsyncIOMotorClient("mongodb://localhost:27017")


async def run_db():
    # Initialize beanie with the Product document class
    await init_beanie(
        database=client.jdanbot,
        document_models=[PidorEvent, PidorEvents, Pidor, Chat, User, Command],
    )

    # await Chat(tg_id=-100500, username="ancaptein", title="ancapistan").create()
    # await User(
    #     tg_id=607998773, username="leno", first_name="le", last_name="no"
    # ).create()
    member = Member(id="607998773@-100500", tg_id=607998773, is_admin=False, name="ancopf")
    chat = await Chat.find_one(Chat.tg_id == -100500)
    print(chat)
    # await chat.update(Push({
    #     Chat.members: member
    # }))
    member2 = Member(id="6079987735@-100500", tg_id=6079987735, is_admin=False, name="ancap")
    # await chat.update(Push({
    #     Chat.members: member2
    # }))

    # db.customer.aggregate([
    #     [
    #         { $match: { "channels.id": "10000-1" }},
    #         { $unwind: "$channels" },
    #         { $replaceRoot: { newRoot: "$channels" } }
    #     ]
    # ])

    mem = await Chat.aggregate(
        [
            {"$unwind": "$members"},
            {"$match": {"members.name": "ancopf"}},
            {"$replaceRoot": {"newRoot": "$members"}}
        ],
        projection_model=Member
    ).to_list()
    pprint(mem)

    print("Hallo, Welt!")


if __name__ == "__main__":
    asyncio.run(run_db())
