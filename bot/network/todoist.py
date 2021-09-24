import todoist

from ..config import dp, TODOIST
from ..lib import handlers


@dp.message_handler(commands="todoist")
@handlers.only_jdan
@handlers.get_text
async def feature_request(message, request):
    api = todoist.TodoistAPI(TODOIST)
    api.sync()

    api.items.add(request, project_id=2271648646)

    api.commit()
    await message.reply("Фиксирую реквест")
