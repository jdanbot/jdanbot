from typing import TYPE_CHECKING, Optional

from aiogram import types

from ..chat_misc.models import ChatModules, ChatSettings
from .lib import BaseModel
from tortoise import fields
from .command import Command

from .pidor import PidorTop, PidorInTop, PidorEvent, Pidor

from tortoise.contrib.postgres.functions import Random
from tortoise.functions import Count

import pendulum as pdl

if TYPE_CHECKING:
    from .member import Member


class Chat(BaseModel):
    id: int = fields.BigIntField(pk=True)

    title: str = fields.TextField()
    username: Optional[str] = fields.TextField(null=True)

    pidor: fields.ForeignKeyField = fields.ForeignKeyRelation(
        "models.Pidor", null=True
    )

    def __str__(self):
        return self.title

    @staticmethod
    async def get_by(message: types.Message) -> "Chat":
        return (
            await Chat.update_or_create(
                id=message.chat.id,
                defaults=dict(
                    username=message.chat.username,
                    title=message.chat or message.from_user.full_name,
                ),
            )
        )[0]

    async def get_random_pidor(self) -> "Member":
        from .member import Member

        return (
            await Member.filter(
                chat_id=self.id, pidor__is_allowed=True
            )
            .annotate(order=Random())
            .order_by("order")
            .first()
        )

    async def can_run_pidor(self) -> bool:
        if self.pidor_id is None:
            return True

        pidor = await Pidor.get(id=self.pidor_id)
        date = await pidor.get_latest_datetime()

        if date is None:
            return True

        timezone = pdl.timezone("Europe/Moscow")

        next_pidor_day = date.replace(tzinfo=timezone).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + pdl.duration(days=1)

        return pdl.now() >= next_pidor_day

    async def get_top_pidors(
        self, limit: int = 10
    ) -> list[PidorInTop]:
        return PidorTop.validate_python(
            await PidorEvent.annotate(count=Count("id"))
            .filter(chat_id=self.id)
            .group_by("pidor_id")
            .limit(limit)
            .order_by("-count")
            .prefetch_related("pidor__user")
            .values(
                "count",
                first_name="pidor__user__first_name",
                last_name="pidor__user__last_name",
                username="pidor__user__username",
            )
        )

    async def get_commands_count(self) -> int:
        return await Command.filter(chat_id=self.id).count()

    async def get_settings(self) -> ChatSettings:
        from .note import Note

        return ChatSettings(
            reactions=dict(
                rules=dict(
                    text=(
                        note_text := await Note.get(
                            self.id, "__rules__"
                        )
                    ),
                    is_enabled=note_text is not None,
                ),
                delete_joines=True,
            ),
            warns_to_ban=await Note.get(
                self.id,
                "__warns_to_ban__",
                default=3,
                type=lambda x, default: x
                if (x := int(x)) in (3, 5, -1)
                else default,
            ),
            language=await Note.get(
                self.id,
                "__chat_lang__",
                default="ru",
                type=lambda x, default: x
                if x in ("ru", "en", "uk")
                else default,
            ),
        )

    async def get_modules(self) -> ChatModules:
        from .note import Note, str2bool

        bool_params = dict(default=True, type=str2bool)

        return ChatModules(
            is_admin_enabled=await Note.get(
                self.id, "__enable_admin__", **bool_params
            ),
            is_selfmute_enabled=await Note.get(
                self.id, "__enable_selfmute__", **bool_params
            ),
            is_poll_enabled=await Note.get(
                self.id, "enable_poll", **bool_params
            ),
            is_memes_enabled=await Note.get(
                self.id, "__enable_response__", **bool_params
            ),
            is_ban_enabled=await Note.get(
                self.id, "enable_ban_trigger", **bool_params
            ),
        )
