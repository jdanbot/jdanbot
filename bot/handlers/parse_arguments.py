from typing import Callable, Any


from functools import wraps
from aiogram import types

from ..lib.errors import JdanbotError
from ..lib.models import CustomField

from aiogram.filters import CommandObject
from fluentogram import FluentTranslator


def run_if_func(value: Any) -> Any:
    return value() if isinstance(value, Callable) else value


def check_is_last_parameter(name: str, params: list) -> bool:
    if params[-1] == "return":
        del params[-1]

    return name == params[-1]


def parse_arguments_new(
    func: Callable,
):  # sourcery skip: bin-op-identity
    async def wrapper(message: types.message):
        text = message.get_args()
        params = {}

        for name in func.__annotations__.keys():
            if name == "message":
                continue
            elif name == "reply":
                if message.reply_to_message:
                    params |= {name: message.reply_to_message}
                    continue
                else:
                    raise JdanbotError(
                        "errors.command_requires_reply"
                    )

            annotation: CustomField = func.__annotations__[name]

            if getattr(annotation, "__name__", None) == "Article":
                continue

            is_latest_arg = check_is_last_parameter(
                name, list(func.__annotations__.keys())
            )

            if is_latest_arg:
                param = text
            else:
                param, text = f"{text} ".split(" ", maxsplit=1)

            if param.strip() == "":
                if (
                    annotation.can_take_from_reply
                    and message.reply_to_message
                ):
                    param = message.reply_to_message.text
                elif (
                    hasattr(annotation, "default")
                    and annotation.default != "ReallyNone"
                ):
                    param = run_if_func(annotation.default)
                elif (
                    annotation.can_take_from_reply
                    and not message.reply_to_message
                ):
                    raise JdanbotError(
                        "errors.command_requires_reply_or_text"
                    )
                else:
                    raise JdanbotError("errors.command_requires_text")

            try:
                try:
                    params |= {
                        name: annotation.type(param) or (0 / 0)
                    }
                except Exception:
                    params |= {
                        name: annotation.fallback(param) or (0 / 0)
                    }
            except Exception:
                params |= {name: run_if_func(annotation.default)}
                text = f"{param} {text}"

        return await func(message, **params)

    return wrapper


def parse_arguments(limit: int, without_params: bool = False):
    def argument_wrapper(func: Callable):
        @wraps(func)
        async def wrapper(
            message: types.Message,
            _: FluentTranslator,
            command: CommandObject,
            **kwargs,
        ):
            try:
                params = (command.args or "").split(
                    maxsplit=limit - 1
                )
            except AttributeError:
                params_raw = message.data.split()
                params = " ".join(params_raw[1:-1]).split(
                    maxsplit=limit - 1
                )
                params.append(params_raw[-1])

                message = message.message

            if len(params) < limit and not without_params:
                try:
                    await message.reply(
                        _.docs.__get__(func.__name__)(),
                        parse_mode="Markdown",
                    )
                except (AttributeError, TypeError):
                    await message.reply(
                        _.few_args(num=limit),
                        parse_mode="Markdown",
                    )
            else:
                return await func(
                    message, command=command, _=_, *params, **kwargs
                )

        return wrapper

    return argument_wrapper
