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


@router.error()
async def catch_error(
    event: types.ErrorEvent, _: Locale, user_lang: str
):
    message = event.update.message
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

    if err_name in ("NotFound",):
        return await message.reply(bold(_.errors.not_found))

    if err_name in ("JdanbotError",):
        print(event.exception.args[0])
        return await message.reply(
            bold(_.get(event.exception.args[0]))
        )

    if settings.logging_chat is not None:
        reply = message.reply_to_message

        await bot.send_message(
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
                error_small="\n".join(
                    [
                        code(err_name),
                        bold(event.exception),
                    ]
                ),
            ),
            disable_web_page_preview=True,
        )

    if message is None:
        return

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
