import asyncio
import aioschedule

from ..config import settings
from ..schemas import Poll


async def scheduler():
    delay = settings.schedule.delay_seconds

    if settings.schedule.katz_bots:
        aioschedule.every(delay).seconds.do(Poll.close_old)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


def schedule_setup():
    if settings.schedule.katz_bots:
        asyncio.create_task(scheduler())
