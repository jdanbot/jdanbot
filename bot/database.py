from sqlfocus import SQLTable

import datetime
from .config import conn

warns = SQLTable("warns", conn)


async def count_wtbans(user_id, chat_id,
                       period=datetime.timedelta(hours=24)):
    period_bound = int((datetime.datetime.now() - period).timestamp())
    w = await warns.select(where=[
        f"timestamp >= {period_bound}",
        f"{user_id = }", f"{chat_id = }"
    ])

    return len(w)


async def mark_chat_member(user_id, chat_id, admin_id, reason):
    await warns.insert(user_id, admin_id, chat_id,
                       int(datetime.datetime.now().timestamp()), reason)

    await conn.commit()
