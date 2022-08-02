from peewee import SqliteDatabase
from ..config import settings

db = SqliteDatabase(settings.db_path)
