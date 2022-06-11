import asyncio
import aioschedule

from ..config import settings
from ..schemas import Poll
from ..youtube.timer import rss_task


async def scheduler():
    delay = settings.delay

    if settings.schedule.youtube:
        for feed in settings.rss_feeds:
            aioschedule.every(delay).seconds.do(
                rss_task,
                feed["url"],
                feed["feed_id"],
                feed["chat_id"]
            )

    if settings.schedule.katz_bots:
        aioschedule.every(delay).seconds.do(Poll.close_old)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


def schedule_setup():
    if settings.schedule.youtube or settings.schedule.katz_bots:
        asyncio.create_task(scheduler())
