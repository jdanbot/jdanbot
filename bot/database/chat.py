from typing import Literal

import aiosqlite
from aiogram import types
from msgspec import Struct, convert

from ..config.languages import Language
from ._base import Base, queries

# from ..chat_misc.models import ChatModules, ChatSettings


class ChatSettings(Struct, frozen=True):
    enable_admin: bool = True
    warns_to_ban: Literal[-1, 3, 5] = 3

    # enable_admin: bool = True
    enable_welcome: bool = True
    enable_rules: bool = True
    # enable_selfmute: bool = True
    enable_kick_on_join: bool = False  # polish mode

    enable_poll: bool = True
    enable_triggers: bool = True
    enable_twitter_redirect: bool = True

    enable_inline_set_note: bool = False

    # locked_commands: list[str] = []


class Chat(Base):
    id: int

    title: str
    username: str | None
    language: Language

    current_pidor_id: int | None
    settings: ChatSettings

    welcome: str | None = None
    rules: str | None = None

    @staticmethod
    async def get_by(message: types.Message) -> "Chat":
        if message.from_user is None:
            raise KeyError

        async with aiosqlite.connect("tortoise.db") as conn:
            chat = await queries.chat.get_by(
                conn,
                **message.chat.model_dump(
                    include={
                        "id",
                        "title",
                        "username",
                    }
                ),
            )
            await conn.commit()

        return convert(
            [*chat[:3], Language.from_str("ru"), 1, dict()],
            Chat,
        )

    @staticmethod
    async def get(id: int) -> "Chat":
        async with aiosqlite.connect("tortoise.db") as conn:
            chat = await queries.chat.get(conn, id=id)

        # return convert(chat, Chat)
        return convert(
            [*chat[:3], Language.from_str("ru"), 1, dict()],
            Chat,
        )


# class Chat_:
    # id: int | Field[int] = fields.IntField(
    #     default=None, pk=True, repr=False
    # )

    # title: str | Field[str] = fields.TextField()
    # username: str | None | Field[str] = fields.TextField(
    #     null=True
    # )

    # pidor_id: int | Field[int] = fields.IntField(null=True)

    # @classmethod
    # async def find_or_place_in_db(
    #     cls: BaseTable, *args, **kwargs
    # ) -> tuple[BaseTable, bool]:
    #     try:
    #         return await cls.get_or_create(*args, **kwargs)
    #     except Exception:
    #         return await cls.update_or_create(
    #             *args, **kwargs
    #         )

    # async def can_run_pidor(self) -> bool:
    #     from .member import Member

    #     if self.pidor_id is None:
    #         return True

    #     pidor = await Member.get(id=self.pidor_id)
    #     date = await pidor.get_latest_datetime()

    #     if date is None:
    #         return True

    #     timezone = pdl.timezone("Europe/Moscow")

    #     next_pidor_day = date.replace(
    #         tzinfo=timezone
    #     ).replace(
    #         hour=0, minute=0, second=0, microsecond=0
    #     ) + pdl.duration(days=1)

    #     return pdl.now() >= next_pidor_day

    # async def get_commands_count(self) -> int:
    #     return await Command.filter(chat_id=self.id).count()

    # async def get_settings(self) -> "ChatSettings":
    #     from .note import Note

    #     return ChatSettings(
    #         reactions=dict(
    #             rules=dict(
    #                 text=(
    #                     note_text := await Note.get(
    #                         self.id, "__rules__"
    #                     )
    #                 ),
    #                 is_enabled=note_text is not None,
    #             ),
    #             delete_joines=True,
    #         ),
    #         warns_to_ban=await Note.get(
    #             self.id,
    #             "__warns_to_ban__",
    #             default=3,
    #             type=lambda x, default: x
    #             if (x := int(x)) in (3, 5, -1)
    #             else default,
    #         ),
    #         language=await Note.get(
    #             self.id,
    #             "__chat_lang__",
    #             default="ru",
    #             type=lambda x, default: x
    #             if x in ("ru", "en", "uk")
    #             else default,
    #         ),
    #     )

    # async def get_modules(self) -> "ChatModules":
    #     from .note import Note, str2bool

    #     bool_params = dict(default=True, type=str2bool)

    #     return ChatModules(
    #         is_admin_enabled=await Note.get(
    #             self.id, "__enable_admin__", **bool_params
    #         ),
    #         is_selfmute_enabled=await Note.get(
    #             self.id,
    #             "__enable_selfmute__",
    #             **bool_params,
    #         ),
    #         is_poll_enabled=await Note.get(
    #             self.id, "enable_poll", **bool_params
    #         ),
    #         is_memes_enabled=await Note.get(
    #             self.id,
    #             "__enable_response__",
    #             **bool_params,
    #         ),
    #         is_ban_enabled=await Note.get(
    #             self.id, "enable_ban_trigger", **bool_params
    #         ),
    #     )
