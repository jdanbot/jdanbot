from typing import Any, Literal

from aiogram import types
from aiosqlite import Row
from msgspec import Struct, convert, json
from pypika import PostgreSQLQuery as Query

from ..config.languages import Language
from ._base import Base, BetterConnection, dbmethod
from ._extras import Json, JsonSet
from ._tables import C


class ChatSettings(Struct, frozen=True, omit_defaults=True):
    enable_welcome: bool = True
    enable_rules: bool = True

    enable_admin: bool = True
    admin_chat: int = 0
    enable_captcha: bool = False

    warns_to_ban: Literal[-1, 3, 5] = 3
    enable_selfmute: bool = True
    enable_kick_on_join: bool = False  # polish mode

    enable_poll: bool = True
    enable_triggers: bool = False  # maybe memes?
    enable_twitter_redirect: bool = False

    enable_inline_set_note: bool = False
    enable_extra_poll_option: bool = False

    locked_commands: list[str] = []


class Chat(Base, frozen=True):
    id: int

    username: str | None
    title: str
    language: Language | None

    current_pidor_id: int | None
    settings: ChatSettings

    welcome: str | None = None
    rules: str | None = None

    @staticmethod
    def __parse(chat: list[Any] | Row) -> "Chat":
        return convert(
            [
                *chat[:3],
                (
                    Language.from_str(chat[-3])
                    if chat[-3]
                    else None
                ),
                chat[-2],
                json.decode(
                    chat[-1] or "{}",
                    type=ChatSettings,
                    strict=False,
                ),
            ],
            Chat,
        )

    @staticmethod
    @dbmethod
    async def get_by(
        message: types.Message,
        conn: BetterConnection,
    ) -> "Chat":
        if message.from_user is None:
            raise KeyError

        chat = await conn.execute_first(
            Query.into(C)  # type: ignore[operator]
            .columns(C.id, C.title, C.username)
            .insert(
                message.chat.id,
                message.chat.full_name,
                message.chat.username,
            )
            .on_conflict(C.id)
            .do_update(C.title)
            .do_update(C.username)
            .returning("*")
        )
        await conn.commit()

        return Chat.__parse(chat)

    @staticmethod
    @dbmethod
    async def get(
        id: int,
        conn: BetterConnection,
    ) -> "Chat":
        chat = await conn.execute_one(
            Query.from_(C).select("*").where(C.id == id)
        )
        assert chat

        return Chat.__parse(chat)

    @staticmethod
    @dbmethod
    async def get_settings(
        id: int, conn: BetterConnection
    ) -> ChatSettings:
        _ = await conn.execute_scalar(
            Query.from_(C)
            .select(C.settings)
            .where(C.id == id)
        )

        return json.decode(_, type=ChatSettings)

    @dbmethod
    async def set_setting_raw(
        self,
        setting: str,
        value: Any,
        conn: BetterConnection,
    ):
        await conn.execute_raw(
            Query.update(C)
            .set(
                C.settings,
                JsonSet(
                    C.settings, f"$.{setting}", Json(value)
                ),
            )
            .where(C.id == self.id)
        )

        await conn.commit()

    @dbmethod
    async def set_setting(
        self,
        setting: str,
        value: Any,
        conn: BetterConnection,
    ):
        try:
            value = float(value)

            if float(value) == int(value):
                value = int(value)
        except ValueError:
            pass

        getattr(ChatSettings, setting)
        convert({setting: value}, ChatSettings)

        await self.set_setting_raw(
            setting, value, conn=conn
        )

    @dbmethod
    async def set_bool_setting(
        self,
        setting: str,
        value: bool,
        conn: BetterConnection,
    ):
        assert isinstance(value, bool)

        await self.set_setting_raw(
            setting, value, conn=conn
        )

    @dbmethod
    async def set_list_setting(
        self,
        setting: str,
        value: list | set,
        conn: BetterConnection,
    ):
        js = json.encode(value).decode("utf-8")
        await self.set_setting_raw(setting, js, conn=conn)

    @dbmethod
    async def set_language(
        self, lang: str, conn: BetterConnection
    ):
        await conn.execute_raw(
            Query.update(C)
            .set(C.language, lang)
            .where(C.id == self.id)
        )
        await conn.commit()

    @staticmethod
    @dbmethod
    async def get_language(
        chat_id: int, conn: BetterConnection
    ) -> Language:
        return await conn.execute_scalar(
            Query.from_(C)
            .select(C.language)
            .where(C.id == chat_id)
        )
