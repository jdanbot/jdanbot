from ..config import dp

@dp.message_handler(commands=["donate"])
async def donate(message):
    await message.reply("<b>Визит очка (через umoney ака Я.Деньги):</b>"
                        "\n\nhttps://yoomoney.ru/to/41001911960333",
                        parse_mode="HTML",
                        disable_web_page_preview=True)
