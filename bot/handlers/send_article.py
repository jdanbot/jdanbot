from aiogram import types


def send_article(func):
    async def wrapper(message: types.Message, *args):
        result = await func(message, *args)

        if result.image:
            await message.answer_chat_action("upload_photo")
            await message.reply_photo(
                result.image,
                caption=result.text,
                parse_mode=result.parse_mode,
                reply_markup=result.keyboard,
                disable_web_page_preview=result.disable_web_page_preview
            )
        else:
            if isinstance(message, types.CallbackQuery):
                message = message.message
                message.reply = message.edit_text

            await message.reply(
                result.text,
                parse_mode=result.parse_mode,
                disable_web_page_preview=result.disable_web_page_preview,
                reply_markup=result.keyboard,
            )

    return wrapper
