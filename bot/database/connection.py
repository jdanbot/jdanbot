from peewee_async import Manager

from ..config import DB_PATH
from .lib.async_sqlite import SqliteDatabase, onefor, get_count

db = SqliteDatabase(DB_PATH)

manager = Manager(db)