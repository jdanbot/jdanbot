from .patches import BetterAIOEngine
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient("mongodb://localhost:27017/")
engine = BetterAIOEngine(client=client, database="jdanbot")
