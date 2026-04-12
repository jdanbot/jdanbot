from aiogram import types
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.filters import BaseFilter, CommandObject
from pydantic import BaseModel

from ..config import Locale
from ..lib.errors import JdanbotError


class Arguments(BaseFilter):
    async def __call__(
        self,
        message: types.Message,
        command: CommandObject,
        handler: HandlerObject,
        _: Locale,
    ) -> dict[str, BaseModel]:
        model =handler.callback.__annotations__["args"]

        try:
            model.model_fields
            parse= self.parse
        except AttributeError:
            parse = model.parse
        
        return {
            "args": await parse(
                message=message,
                model=model,
                args=command.args or "",
                _=_,
            )
        }

    @staticmethod
    async def parse(
        message: types.Message,
        model: BaseModel,
        args: str,
        _: Locale,
    ) -> BaseModel:
        params = {}

        for name in model.model_fields:
            field = model.model_fields[name]

            if name == "message":
                params |= {name: message}
                continue
            elif name == "reply":
                params |= {name: message.reply_to_message}
                continue
            elif name == "i18n":
                params |= {name: _}
                continue

            if list(model.model_fields)[-1] == name:
                param = args
            else:
                param, args = f"{args}".split(
                    " ", maxsplit=1
                )

            if param.strip() == "":
                if (
                    field.metadata != []
                    and isinstance(
                        (meta := field.metadata[0]), dict
                    )
                    and (reply := meta.get("reply", False))
                    and message.reply_to_message
                ):
                    param = message.reply_to_message.text
                elif not field.is_required():
                    # skip; went text to previous variant
                    args = param + args
                elif reply and not message.reply_to_message:
                    raise JdanbotError(
                        "errors.command_requires_reply_or_text"
                    )
                else:
                    raise JdanbotError(
                        "errors.command_requires_text"
                    )

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

        return model.model_validate(params)
