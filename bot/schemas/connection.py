from peewee import SqliteDatabase
from ..config import DB_PATH

db = SqliteDatabase(DB_PATH)
