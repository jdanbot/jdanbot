from aiogram import types
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.filters import BaseFilter, CommandObject
from pydantic import BaseModel

from ..lib.errors import JdanbotError


class Arguments(BaseFilter):
    async def __call__(
        self,
        message: types.Message,
        command: CommandObject,
        handler: HandlerObject,
    ) -> dict[str, BaseModel]:
        model: BaseModel = handler.callback.__annotations__["args"]

        text = command.args or ""
        params = {}

        for name in model.model_fields:
            field = model.model_fields[name]

            if name == "message":
                params |= {name: message}
                continue
            elif name == "reply":
                params |= {name: message.reply_to_message}
                continue

            if list(model.model_fields)[-1] == name:
                param = text
            else:
                param, text = f"{text} ".split(" ", maxsplit=1)

            if param.strip() == "":
                if (
                    field.metadata != []
                    and isinstance((meta := field.metadata[0]), dict)
                    and (reply := meta.get("reply", False))
                    and message.reply_to_message
                ):
                    param = message.reply_to_message.text
                elif not field.is_required():
                    # skip; went text to previous variant
                    text = param + text
                elif reply and not message.reply_to_message:
                    raise JdanbotError(
                        "errors.command_requires_reply_or_text"
                    )
                else:
                    raise JdanbotError("errors.command_requires_text")

            if param:
                params |= {name: param}
            # try:
            #     try:

            #     except Exception:
            #         params |= {
            #             name: annotation.fallback(param) or (0 / 0)
            #         }
            # except Exception:
            #     params |= {name: run_if_func(annotation.default)}
            #     text = f"{param} {text}"

        return {"args": model.model_validate(params)}
