from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from .telegram import PidorEvent, PidorEvents, Pidor, Chat, User, Member
from .command import Command
import asyncio


client = AsyncIOMotorClient("mongodb://localhost:27017")

async def run_db():
    # Initialize beanie with the Product document class
    await init_beanie(database=client.jdanbot, document_models=[
        PidorEvent, PidorEvents, Pidor, Chat, User, Member,
        Command
    ])
    
    print("Hallo, Welt!")

    await PidorEvents(
        pidor_id=0,
        events=[]
    ).save()

    chat = await Chat.get_or_create(dict(
        tgid=100,
        title="ANCAP"
    ))


if __name__ == "__main__":
    asyncio.run(run_db())