from ..config import dp


@dp.message_handler(commands=["donate"])
async def donate(message):
    await message.reply("<b>🇷🇺 UMoney aka Я.Деньги:</b> 5599 0050 8875 2808",
                        parse_mode="HTML",
                        disable_web_page_preview=True)
