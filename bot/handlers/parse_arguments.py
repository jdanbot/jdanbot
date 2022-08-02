from ..config import _


from functools import wraps


def parse_arguments(limit, without_params=False):
    def argument_wrapper(func):
        @wraps(func)
        async def wrapper(message):
            try:
                params = message.get_full_command()[1].split(maxsplit=limit - 1)
            except AttributeError:
                params_raw = message.data.split()
                params = " ".join(params_raw[1:-1]).split(maxsplit=limit - 1)
                params.append(params_raw[-1])

                message = message.message

            if len(params) < limit and not without_params:
                try:
                    await message.reply(_(f"docs.{func.__name__}"), parse_mode="Markdown")
                except AttributeError:
                    await message.reply(
                        _("errors.few_args", num=limit), parse_mode="Markdown"
                    )
            else:
                return await func(message, *params)

        return wrapper

    return argument_wrapper
