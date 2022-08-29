import pendulum as pdl

from .connection import db
from .pidor import Pidor

from aiogram import types
from peewee import CharField, ForeignKeyField, Model

from ..chat_misc.models import ChatSettings, ChatModules


class Chat(Model):
    username = CharField(null=True)
    title = CharField(null=True)
    pidor = ForeignKeyField(Pidor, null=True, column_name="pidor_of_day_id")

    class Meta:
        db_table = "chats"
        database = db

    @property
    def all_pidors(self) -> list[Pidor]:
        from .chat_member import ChatMember

        return list(
            Pidor.select()
            .join(ChatMember, on=ChatMember.pidor_id == Pidor.id)
            .join(Chat, on=ChatMember.chat_id == Chat.id)
            .where(Chat.id == self.id, Pidor.is_pidor_allowed == True)
        )

    @property
    def can_run_pidor_finder(self) -> bool:
        if self.pidor is None:
            return True

        if isinstance(self.pidor.when_pidor_of_day, str):
            when_pidor_of_day = pdl.parse(self.pidor.when_pidor_of_day)
        else:
            when_pidor_of_day = self.pidor.when_pidor_of_day

        timezone = pdl.timezone("Europe/Moscow")

        next_pidor_day = when_pidor_of_day.replace(tzinfo=timezone).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + pdl.duration(days=1)

        return pdl.now(timezone) >= next_pidor_day

    def get_by_message(message: types.Message) -> "Chat":
        chat = message.chat
        defaults = dict(title=chat.title, username=chat.username)

        if chat.id > 0:
            chat.title = message.from_user.full_name

        Chat.get_or_create(id=chat.id, defaults=defaults)
        Chat.update(**defaults).where(Chat.id == chat.id).execute()

        return Chat.get_by_id(chat.id)

    def get_settings(self) -> ChatSettings:
        from .note import Note

        return ChatSettings(
            reactions=dict(
                rules=dict(
                    text=(note_text := Note.get(self.id, "__rules__")),
                    is_enabled=note_text is not None
                ),
                delete_joines=True
            ),

            warns_to_ban=Note.get(
                self.id,
                "__warns_to_ban__",
                default=3,
                type=lambda x, default: x if (x := int(x)) in (3, 5, -1) else default
            ),
            language=Note.get(
                self.id,
                "__chat_lang__",
                type=lambda x, default: x if x in ("ru", "en", "uk") else default
            )
        )

    def get_modules(self) -> ChatModules:
        from .note import Note, str2bool

        bool_params = dict(default=True, type=str2bool)

        return ChatModules(
            is_admin_enabled=Note.get(self.id, "__enable_admin__", **bool_params),
            is_selfmute_enabled=Note.get(self.id, "__enable_selfmute__", **bool_params),
            is_poll_enabled=Note.get(self.id, "enable_poll", **bool_params),

            is_memes_enabled=Note.get(self.id, "__enable_response__", **bool_params),
            is_ban_enabled=Note.get(self.id, "enable_ban_trigger", **bool_params),
        )
