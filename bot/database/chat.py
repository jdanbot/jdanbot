from typing import TYPE_CHECKING, Optional

from aiogram import types
from piccolo.query import OrderByRaw
from piccolo.query.methods.select import Count
from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..chat_misc.models import ChatModules, ChatSettings
from . import tables as t
from .lib import IdModel, unpack_needen
from .command import Command

from .pidor import PidorTop


if TYPE_CHECKING:
    from .member import Member


class Chat(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: Optional[str] = Field(default=None)
    title: str

    chat: list["Member"] = Relationship(
        # back_populates="chat"
    )
    # pidor: Optional["Member"] | int = None

    @staticmethod
    async def get_by(
        conn: AsyncSession, message: types.Message
    ) -> IdModel:
        return await conn.merge(
            Chat(
                **unpack_needen(
                    message.chat,
                    {"id", "username"},
                ),
                title=message.chat.title
                or message.from_user.full_name,
            )
        )

    async def get_random_pidor(self) -> "Member":
        return Member.parse_obj(
            await t.Member.select(
                t.Member.id,
                t.Member.pidor.all_columns(),
                t.Member.user.all_columns(),
                t.Member.chat.all_columns(),
            )
            .where(t.Member.chat == self.id)
            .where(
                t.Member.pidor._.is_allowed.eq(True),
            )
            .order_by(OrderByRaw("random()"))
            .first()
            .output(nested=True)
        )

    async def get_pidor_count(self) -> int:
        return await (
            t.Member.count()
            .where(t.Member.chat.id == self.id)
            .where(t.Member.pidor.is_not_null())
            .where(t.Member.pidor._.is_allowed.eq(True))
        )

    async def can_run_pidor(self) -> bool:
        if self.pidor is None:
            return True

        pidor = Pidor.parse_obj(
            await t.Pidor.select()
            .where(t.Pidor.id == self.pidor)
            .first()
        )

        date = await pidor.get_latest_datetime()

        if date is None:
            return True

        timezone = pdl.timezone("Europe/Moscow")

        next_pidor_day = date.replace(tzinfo=timezone).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + pdl.duration(days=1)

        return pdl.now() >= next_pidor_day

    async def get_top_pidors(self, limit: int = 10) -> list[PidorTop]:
        return PidorTop.from_list(
            await t.PidorEvent.select(
                Count(),
                t.PidorEvent.pidor.id,
                t.PidorEvent.pidor.user._.all_columns(),
            )
            .where(t.PidorEvent.chat.id == self.id)
            .group_by(t.PidorEvent.pidor)
            .order_by(OrderByRaw("count"), ascending=False)
            .limit(limit)
            .output(nested=True)
        )

    async def get_members_count(self, conn: AsyncSession) -> int:
        res = await conn.exec(
            select(func.count(Chat.id)).where(Chat.id == self.id)
        )

        return res.first()

    async def get_commands_count(self, conn: AsyncSession) -> int:
        res = await conn.exec(
            select(func.count(Command.id)).where(
                Command.chat_id == self.id
            )
        )

        return res.first()

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
