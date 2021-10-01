from peewee import SqliteDatabase

from ..config import DB_PATH

db = SqliteDatabase(DB_PATH)
manager = None
get_count = None
