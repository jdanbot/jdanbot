from ..config import dp

from aiogram.types import ContentType


@dp.message_handler(lambda x: x.forward_from_chat and

                              (x.from_user.id in (675257916,) and
                               x.forward_from_chat.id in (-1001113237212,)) or

                              (x.forward_from_chat.id in (-1001204336102,) and
                               x.chat.id in (-1001176998310, -1001410092459)),
                    content_types=ContentType.ANY)
async def unknown_message(message):
    await message.delete()