import time
from random import choice, randint

from aiogram import F, types

from ..config import bot, router
from ..database.chat import ChatSettings
from ..filters import Check, WithRandom
from .legacy import triggers


def smart_split(x: str) -> list[str] | None:
    if x is None:
        return None

    return x.split(" ")


space = r"[^a-zа-яё\d]"
BAN_REGEXP = (
    rf"(^|{space})[бb][\W]*[аaα@🅰️][\W]*[нnh🅱️]({space}|$)"
)
NAKI_REGEXP = rf"(^|{space})наки({space}|$)"


@router.message(
    F.text.lower().startswith("бот, сколько ")
    & F.text.endswith("?"),
    Check(ChatSettings.enable_triggers),
)
async def random_answer(message: types.Message):
    assert message.text
    number = randint(0, 1000)

    word = message.text.lower()[:-1].split(" ")[2:][0]
    await message.reply(f"{number} {word}")


@router.message(
    F.reply_to_message.from_user.id.in_([1121412322])
    & F.text.lower().func(smart_split).contains("спасибо"),
)
async def duakyu(message: types.Message):
    await message.reply_sticker(
        "CAACAgIAAx0CRieRpgABA7bCX1aW70b_1a0OspsDDXYk8iPACEkAArwBAAKUmWkvXbzmLd8q5dcbBA"
    )


@router.message(
    F.text.lower().func(smart_split).contains("секс")
    | F.text.lower().func(smart_split).contains("кфс"),
    WithRandom(),
    Check(ChatSettings.enable_triggers),
)
async def who(message: types.Message):
    await message.reply("Что?")


@router.message(
    F.text.lower().func(smart_split).contains("бойкот"),
    WithRandom(),
    Check(ChatSettings.enable_triggers),
)
async def boikot(message: types.Message):
    await message.reply(triggers["boikot"])


@router.message(
    F.text.lower().regexp(NAKI_REGEXP, search=True),
    WithRandom(),
    Check(ChatSettings.enable_triggers),
)
async def naki(message):
    await message.reply("Майкл Наки — в жопе козинаки")


@router.message(
    F.text.lower().func(smart_split).contains("яблоко")
    | F.text.lower().func(lambda x: x.find("яблочн") != -1),
    WithRandom(),
    Check(ChatSettings.enable_triggers),
)
async def apple(message: types.Message):
    await message.reply(triggers["apple"])


@router.message(
    F.text.lower().regexp(BAN_REGEXP),
    Check(ChatSettings.enable_triggers),
)
async def get_a_ban(message: types.Message):
    messages = triggers["ban_messages"]
    user_id = message.from_user.id if message.from_user else 0

    words = (
        messages.get(str(user_id))
        or messages["all"]
    )

    word = choice(words)

    if isinstance(word, str):
        await message.reply(
            word,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    elif isinstance(word, dict):
        await message.reply(word["text"], parse_mode="HTML")
        await message.answer_sticker(word["sticker"])

    try:
        await bot.restrict_chat_member(
            message.chat.id,
            user_id,
            until_date=int(time.time() + 60),
            permissions=types.ChatPermissions(
                can_send_messages=True
            ),
        )
    except Exception:
        pass


@router.message(
    F.text.lower().startswith("бот, почему")
    & F.text.endswith("?"),
    Check(ChatSettings.enable_triggers),
)
async def why_list(message: types.Message):
    await message.reply(choice(triggers["why_list"]))


@router.message(
    F.text.lower().startswith("бот,")
    & F.text.func(
        lambda text: " или " in text or " чи " in text
    ),
    Check(ChatSettings.enable_triggers),
)
async def question(message):
    text = (
        message.text.lower()
        .removeprefix("бот,")
        .removesuffix("?")
    )
    cuts = (
        cuts
        if len(cuts := text.split(" или ")) > 1
        else text.split(" чи ")
    )

    await message.reply(choice(cuts).strip().capitalize())


@router.message(
    F.text.lower().startswith("бот,"),
    Check(ChatSettings.enable_triggers),
)
async def all_question(message: types.Message):
    await message.reply(choice(["Да", "Нет"]))
