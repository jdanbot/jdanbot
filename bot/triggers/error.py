import traceback
from datetime import datetime

from aiogram import types
from aiogram.utils.markdown import bold, code

from ..config import LANGS, bot, router, settings
from ..config.lib.locales import Locale

log_schema = """
{name} [{id}]

*lang*: {locale}
*reply*: {reply}
*query*: {query}

{error_small}
"""

error_file_template = '<meta name="viewport" content="width=device-width, initial-scale=1"><pre>{trace}</pre>'


@router.error()
async def catch_error(
    event: types.ErrorEvent, _: Locale, user_lang: str
):
    message = event.update.message
    assert message

    err_name = event.exception.__class__.__name__

    if err_name in (
        "MessageCantBeDeleted",
        "BadRequest",
        "MessageTextIsEmpty",
        "BotKicked",
        "TimeoutError",
        "CantRestrictChatOwner",
        "UserIsAnAdministratorOfTheChat",
        "NotEnoughRightsToRestrict",
    ):
        return

    if err_name == "NotFound":
        return await message.reply(bold(_.errors.not_found))

    if err_name == "JdanbotError":
        print(event.exception.args[0])
        return await message.reply(
            bold(_.get(event.exception.args[0]))
        )

    if settings.logging_chat is not None:
        reply = message.reply_to_message

        m = await bot.send_message(
            settings.logging_chat,
            log_schema.format(
                name=bold(message.chat.full_name),
                id=code(message.chat.id),
                user=message.from_user.mention_markdown(),
                user_id=code(message.from_user.id),
                locale=LANGS[user_lang].emoji,
                query=code(message.text),
                reply=code(reply.content_type.value)
                if reply is not None
                else "❌",
                error_small=code(err_name),
            ),
            disable_web_page_preview=True,
        )
        await m.reply_document(
            types.BufferedInputFile(
                error_file_template.format(
                    trace=traceback.format_exc()
                ).encode("utf-8"),
                filename=f"{datetime.now()}.html",
            )
        )

    await message.reply(
        "\n".join(
            [
                bold(_.errors.template),
                code(
                    event.exception.__str__().split("\n")[0]
                ),
            ]
        )
    )

    raise event.exception
