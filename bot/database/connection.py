from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from telegram import PidorEvent, PidorEvents, Pidor
import asyncio



client = AsyncIOMotorClient("mongodb://localhost:27017")

async def run_db():
    # Initialize beanie with the Product document class
    await init_beanie(database=client.jdanbot, document_models=[
        PidorEvent, PidorEvents, Pidor
    ])
    
    print("Hallo, Welt!")

    await PidorEvents(
        pidor_id=0,
        events=[]
    ).save()


if __name__ == "__main__":
    asyncio.run(run_db())