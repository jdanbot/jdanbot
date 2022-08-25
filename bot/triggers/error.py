import traceback

from aiogram import types

from aiogram.utils.markdown import bold, code

from ..config import dp, bot, _, settings, LANGS


log_schema = """
{name} [{id}]

*lang*: {locale}
*reply*: {reply}
*query*: {query}

{error_small}
"""


@dp.errors_handler()
async def catch_error(callback: types.CallbackQuery, exception: str):
    message = callback.message

    error = traceback.format_exc()
    inf_err = error.split("\n")[-2]

    exc_full = inf_err.split(":")[0]
    exc = exc_full.split(".")[-1]

    if exc in (
        "MessageCantBeDeleted",
        "BadRequest",
        "MessageCantBeDeleted",
        "MessageTextIsEmpty",
        "BotKicked",
        "TimeoutError",
        "CantRestrictChatOwner",
        "UserIsAnAdministratorOfTheChat",
        "NotEnoughRightsToRestrict",
    ):
        return

    if exc in ("NotFound",):
        await message.reply(bold(_("errors.not_found")), parse_mode="MarkdownV2")
        return

    if settings.logging_chat is not None:
        reply = message.reply_to_message

        await bot.send_message(
            settings.logging_chat,
            log_schema.format(
                name=bold(message.chat.full_name),
                id=code(message.chat.id),

                user=message.from_user.get_mention(),
                user_id=code(message.from_user.id),

                locale=LANGS[lang].emoji if (lang := _(None, return_lang=True)) is not None else lang,
                query=code(message.text),
                reply=reply.content_type if reply is not None else "❌",

                error_small="   ".join(map(code, inf_err.split(": ")))
            ),
            parse_mode="MarkdownV2",
        )

    if message is None:
        return

    await message.reply(
        bold(_("errors.error")) + "\n" + code(exception), parse_mode="MarkdownV2"
    )
