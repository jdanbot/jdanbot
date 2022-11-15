from ..config import dp

from aiogram import types


@dp.message_handler(
    lambda x: x.forward_from_chat
    and x.chat.id in (-1001176998310,)
    and (
        (
            x.from_user.id in (675257916, 811510365)
            and x.forward_from_chat.id in (-1001113237212,)
        )
        or (x.forward_from_chat.id in (-1001204336102,))
        or (
            x.from_user.id in (
                # 1890967276,
                679350651,
            )
            and x.forward_from_chat.id < 0
        )
    ),
    content_types=types.ContentType.ANY,
)
async def just_blocker(message: types.Message):
    await message.delete()
