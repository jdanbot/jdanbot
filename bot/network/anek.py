from ..config import dp
from ..lib.anekru import Anekru


@dp.message_handler(commands=["anek", "anekru"])
async def anekru_command(message):
    anekru = Anekru()
    anek = await anekru.get_random()

    await message.reply(anek)
