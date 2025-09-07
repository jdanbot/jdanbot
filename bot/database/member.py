from typing import Any, override

import pendulum as pdl
from aiogram import types
from aiogram.utils.markdown import hlink, link
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from pypika_tortoise.functions import Count
from tortoise.contrib.postgres.functions import Random

from bot.lib.admin import check_admin

from ..config.bot import bot
from .chat import Chat
from .pidor import Pidor, PidorEvent, PidorInTop, PidorTop
from .user import User

# from .warn import Warn
# from .user import User


class Member(BaseModel):
    user_id: int
    chat_id: int

    lang: str = "ru"

    first_name: str
    last_name: str | None = None
    username: str | None = None

    # user: types.User = Field(repr=False, default=None)
    chat: Chat = Field(repr=False, default=None)

    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True
    )

    @override
    def __str__(self):
        return f"Member {self.user_id}@{self.chat_id}"

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join(
                [self.first_name, self.last_name]
            )

        return self.first_name

    @property
    def mention(self) -> str:
        return self.username or self.full_name

    @property
    def tag(self, use_html: bool = False) -> str:
        if self.username:
            return f"@{self.username}"

        return (hlink if use_html else link)(
            self.full_name,
            f"tg://user?id={self.user_id}",
        )

    @classmethod
    async def get_by(
        cls, message: types.Message
    ) -> "Member":
        chat: Chat = await Chat.get_by(message)
        user: User = await User.get_by(message)

        return Member(
            user_id=user.id,
            chat_id=chat.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            # user=message.from_user,  # type: ignore
            chat=chat,
        )

    @classmethod
    async def get(
        cls, user_id: int, chat_id: int
    ) -> "Member":
        chat: Chat = await Chat.get(id=chat_id)
        user: User = await User.get(id=user_id)

        return Member(
            user_id=user.id,
            chat_id=chat.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            chat=chat,
        )

    ############ NOTES ############

    @classmethod
    async def get_note(
        cls, name: str, default: Any = None
    ) -> Any:
        return None or default

    ############ PIDOR ############

    async def is_pidor(self) -> bool:
        try:
            return bool(
                await Pidor.get(
                    chat_id=self.chat_id,
                    user_id=self.user_id,
                )
            )
        except:
            return False

    async def get_is_already_pidor(self) -> bool:
        if await self.is_pidor():
            return False

        return bool(await self.update(is_pidor=True))

    async def find_new_pidor(self) -> "Member | bool":
        return False

    async def get_pidor(self) -> tuple[Pidor, bool]:
        return await Pidor.get_or_create(
            chat_id=self.chat_id,
            user_id=self.user_id,
        )

    async def get_random_pidor(self) -> Pidor:
        pidor = (
            await Pidor.filter(
                chat_id=self.chat_id, is_allowed=True
            )
            .annotate(order=Random())
            .order_by("order")
            .first()
        )

        return pidor

    async def get_status(self) -> str:
        return (
            await bot.get_chat_member(
                self.chat_id, self.user_id
            )
        ).status

    async def is_left(self) -> bool:
        return await self.get_status() == "left"

    async def get_pidor_count(self) -> int:
        return await Pidor.filter(
            chat_id=self.chat_id, is_allowed=True
        ).count()

    async def get_top_pidors(
        self, limit: int = 10
    ) -> list[PidorInTop]:
        return PidorTop.validate_python(
            await PidorEvent.annotate(count=Count("id"))
            .filter(chat_id=self.chat_id)
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

    async def check_run_pidor(self) -> bool:
        if self.chat.pidor_id is None:
            return True

        pidor: Pidor = await Pidor.get(
            id=self.chat.pidor_id
        )
        date: (
            DateTime | None
        ) = await pidor.get_latest_datetime()

        if date is None:
            return True

        timezone: Timezone = pdl.timezone("Europe/Moscow")

        next_pidor_day: DateTime = date.replace(
            tzinfo=timezone
        ).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + pdl.duration(days=1)

        return pdl.now() >= next_pidor_day

    async def get_members_count(self) -> int:
        return -1

    async def get_in_chats_count(self) -> int:
        return -1
        return await Member.filter(user_id=self.user.id).count()

    async def get_pidor_events_count(self) -> int:
        pidor = await Pidor.get(user_id=self.user_id, chat_id=self.chat_id)
        return await PidorEvent.filter(pidor_id=pidor.id).count()

    async def check_admin(self) -> bool:
        return True
        return await check_admin(
            bot,
            self.chat_id,
            self.user_id,
        )

    async def warn(self, *args, **kwargs):
        return


#         return self.is_admin or False
# class Member_old(ormar.Model):
#     # ormar_config = base_ormar_config.copy(tablename="members")

#     # id: int = ormar.Integer(primary_key=True)
#     # chat = ormar.ForeignKey(Chat, skip_reverse=True)
#     # user: User = ormar.ForeignKey(User, skip_reverse=True)

#     # is_admin: Optional[bool] = ormar.Boolean(nullable=True)
#     # is_pidor: bool = ormar.Boolean(nullable=True)

#     # last_pidor: PidorEvent = ormar.ForeignKey(PidorEvent)

#     # warns: fields.ReverseRelation
#     # warned: fields.ReverseRelation

#     @classmethod
#     async def filter(cls, *args, **kwargs):
#         return cls.filter(*args, **kwargs)

#     async def check_admin(self) -> bool:
#         await self.update(is_admin=await check_admin(bot, self.chat_id, self.user_id))

#         return self.is_admin or False

#     @staticmethod
#     async def get_by(message: types.Message) -> "Member":
#         return (
#             await Member.get_or_create(
#                 chat=(await Chat.get_by(message)).id,
#                 user=(await User.get_by(message)).id,
#             )
#         )[0]

#     @staticmethod
#     async def get_by_id(id: int) -> "Member":
#         return await Member.get(id=id)

#     async def get_latest_datetime(self) -> pdl.DateTime | None:
#         if self.last_pidor is None:
#             return None

#         return (await self.last_pidor.load()).caused_at


#     @staticmethod
#     async def get_id_by(message: types.Message) -> int:
#         return (await Member.get_by(message)).id

#     async def get_pidor_events_count(self) -> int:
#         return await PidorEvent.filter(pidor_id=self.id).count()


#     async def get_in_chats_count(self) -> int:
#         return await Member.filter(user_id=self.user.id).count()

#     async def warn(self, victim: "Member", reason: str) -> Warn:
#         return await Warn.create(
#             who_warn_id=self.id,
#             who_warned_id=victim.id,
#             reason=reason,
#         )
