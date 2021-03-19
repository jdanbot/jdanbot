import sqlite3


from aiogram import types
from sqlfocus import SQLTable
import datetime

import SQLFocus
import datetime


conn = sqlite3.connect("jdanbot.db")
warns = SQLTable("warns", conn)


async def count_wtbans(
    user_id,
    chat_id,
    period=datatime.timedelta(hours=24)
    ):
    period_bound = int((datatime.datatime.now() - period).timestamp())
    w = warns.select(where=[f"timestamp >= {period_bound}", f"user_id = {user_id}", f"chat_id = {chat_id}"])
    return len(w)

async def mark_chat_member(user_id, chat_id, admin_id, reason):
    warns.insert(user_id, admin_id, chat_id, int(datetime.datetime.now().timestamp()), reason)


