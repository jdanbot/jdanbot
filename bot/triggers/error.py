import traceback
import io

from ..config import dp, bot, _, settings
from ..lib.text import fixHTML, bold, code


log_schema = """
{name} #{id}
<b>query:</b> {query}

#{error_small}
"""


@dp.errors_handler()
async def catch_error(callback, exception):
    message = callback.message
    error = traceback.format_exc()
    inf_err = error.split("\n")[-2]

    exc = inf_err.split(":")[0].split(".")[-1]

    if exc in ("MessageCantBeDeleted", "BadRequest", "MessageCantBeDeleted",
               "MessageTextIsEmpty", "BotKicked", "TimeoutError",
               "CantRestrictChatOwner", "UserIsAnAdministratorOfTheChat",
               "NotEnoughRightsToRestrict"):
        return

    if settings.logging_chat is not None:
        f = io.StringIO(error)
        f.name = f"{exc}.log"

        if message.chat.id < 0:
            id = str(message.chat.id).replace("-100", "chat")
        else:
            id = f"user{message.chat.id}"

        await bot.send_document(
            settings.logging_chat, document=f,
            caption=log_schema.format(
                name=bold(getattr(message.chat, "first_name") or
                          message.chat.title),
                query=fixHTML(message.text),
                error_small=inf_err,
                id=id
            ),
            parse_mode="HTML"
        )

    if message is None:
        return

    await message.reply(bold(_("errors.error")) + "\n"
                        + code(inf_err),
                        parse_mode="HTML")
