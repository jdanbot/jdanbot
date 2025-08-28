from typing import override

import pendulum as pdl
from aiogram import types
from tortoise import fields
from tortoise.fields import Field

from .command import Command
from .lib.base_table import BaseTable
from .pidor import PidorEvent, PidorInTop, PidorTop

# from ..chat_misc.models import ChatModules, ChatSettings


class Chat(BaseTable):
    id: int | Field[int] = fields.IntField(
        default=None, pk=True, repr=False
    )

    title: str | Field[str] = fields.TextField()
    username: str | None | Field[str] = fields.TextField(
        null=True
    )

    # pidor_events: list[PidorEvent] = ormar.ManyToMany(
    #     PidorEvent, related_name="pidor_events"
    # )

    pidor_id: int | Field[int] = fields.IntField(null=True)

    # pidor: fields.ForeignKeyRelation[Pidor] = fields.ForeignKeyField(
    #     "models.Pidor", null=True
    # )
    # pidor_id: int

    @classmethod
    async def find_or_place_in_db(
        cls: BaseTable, *args, **kwargs
    ) -> tuple[BaseTable, bool]:
        try:
            return await cls.get_or_create(*args, **kwargs)
        except Exception:
            return await cls.update_or_create(
                *args, **kwargs
            )

    @staticmethod
    async def get_by(message: types.Message) -> "Chat":
        return (
            await Chat.update_or_create(
                id=message.chat.id,
                defaults=dict(
                    username=message.chat.username,
                    title=message.chat.title
                    or message.from_user.full_name,
                ),
            )
        )[0]

    async def get_random_pidor(self) -> "Member | None":
        from .member import Member

        table = Member.ormar_config.table

        return await Member.get(
            id=await Member.database.fetch_val(
                select(table)
                .where(
                    table.c.is_pidor == 1,
                    table.c.chat == self.id,
                )
                .order_by(text("RANDOM()"))
            )
        )

    async def can_run_pidor(self) -> bool:
        from .member import Member

        if self.pidor_id is None:
            return True

        pidor = await Member.get(id=self.pidor_id)
        date = await pidor.get_latest_datetime()

        if date is None:
            return True

        timezone = pdl.timezone("Europe/Moscow")

        next_pidor_day = date.replace(
            tzinfo=timezone
        ).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + pdl.duration(days=1)

        return pdl.now() >= next_pidor_day

    async def get_top_pidors(
        self, limit: int = 10
    ) -> list[PidorInTop]:
        from .member import Member
        from .user import User

        # return PidorTop.validate_python(
        #     await PidorEvent.filter(chat_id=self.id)..values()
        # )

        table = PidorEvent.ormar_config.table
        m_table = Member.ormar_config.table
        u_table = User.ormar_config.table
        c = table.c

        res = await PidorEvent.database.fetch_all(
            select(
                func.count(c.id).label("count_1"),
                u_table.c.username,
                u_table.c.first_name,
                u_table.c.last_name,
            )
            .where(c.chat_id == self.id)
            .group_by(c.pidor_id)
            .order_by(text("-count_1"))
            .limit(10)
            .join(
                m_table,
                c.pidor_id == m_table.c.id,
            )
            .join(u_table, m_table.c.user == u_table.c.id)
        )

        return PidorTop.validate_python(
            [
                PidorInTop(
                    count=r[0],
                    username=r[1],
                    first_name=r[2],
                    last_name=r[3],
                )
                for r in res
            ]
        )

    async def get_commands_count(self) -> int:
        return await Command.filter(chat_id=self.id).count()

    async def get_settings(self) -> "ChatSettings":
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

    async def get_modules(self) -> "ChatModules":
        from .note import Note, str2bool

        bool_params = dict(default=True, type=str2bool)

        return ChatModules(
            is_admin_enabled=await Note.get(
                self.id, "__enable_admin__", **bool_params
            ),
            is_selfmute_enabled=await Note.get(
                self.id,
                "__enable_selfmute__",
                **bool_params,
            ),
            is_poll_enabled=await Note.get(
                self.id, "enable_poll", **bool_params
            ),
            is_memes_enabled=await Note.get(
                self.id,
                "__enable_response__",
                **bool_params,
            ),
            is_ban_enabled=await Note.get(
                self.id, "enable_ban_trigger", **bool_params
            ),
        )
