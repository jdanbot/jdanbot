import traceback

from ..config import dp, bot, _, LOGGING_CHAT
from ..lib.text import bold, code


@dp.errors_handler()
async def catch_error(callback, exception):
    error = traceback.format_exc()
    inf_err = error.split("\n")[-2]

    exc = inf_err.split(":")[0].split(".")[-1]

    if exc in ("MessageCantBeDeleted", "BadRequest", "MessageCantBeDeleted",
               "MessageTextIsEmpty", "BotKicked", "TimeoutError",
               "CantRestrictChatOwner", "UserIsAnAdministratorOfTheChat",
               "NotEnoughRightsToRestrict"):
        return

    if LOGGING_CHAT is not None:
        await bot.send_message(LOGGING_CHAT, code(error),
                               parse_mode="HTML")

    if callback.message is None:
        return

    await callback.message.reply(bold(_("errors.error")) + "\n"
                                 + code(inf_err),
                                 parse_mode="HTML")
