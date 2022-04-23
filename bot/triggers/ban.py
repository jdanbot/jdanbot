import re
import time

from random import randint, choice

from ..config import bot, dp, _
from .. import handlers


# TODO: REWRITE: use regular


space = r"[^a-zа-яё\d]"
BAN_REGEXP = rf"(^|{space})[бb][\W]*[аaα@🅰️][\W]*[нnh🅱️]({space}|$)"
NAKI_REGEXP = rf"(^|{space})наки({space}|$)"


@dp.message_handler(lambda msg: msg.text.lower().find("бот, сколько") != -1 and
                    msg.text.lower().find("?") != -1)
@handlers.check("__enable_response__")
async def random_answer(message):
    number = randint(0, 1000)

    word = message.text.lower().replace("бот, сколько", "").split()[0]
    await message.reply(f"{number} {word}")


@dp.message_handler(lambda msg: msg.reply_to_message and
                    msg.reply_to_message.from_user.id in (1121412322,) and
                    msg.text.lower().find("спасибо") != -1)
async def duakyu(message):
    await message.reply_sticker("CAACAgIAAx0CRieRpgABA7bCX1aW70b_1a0OspsDDXYk8iPACEkAArwBAAKUmWkvXbzmLd8q5dcbBA") # noqa


@dp.message_handler(lambda msg: msg.text.lower().find("бот, почему") != -1)
@handlers.check("__enable_response__")
async def why_list(message):
    await message.reply(choice(_("triggers.why_list")))


@dp.message_handler(lambda msg: msg.text.lower().find("секс") != -1 or msg.text.lower().find("кфс") != -1)
@handlers.check("__enable_response__")
@handlers.randomed_start
async def who(message):
    await message.reply("Что?")


@dp.message_handler(lambda msg: msg.text.lower().find("бойкот") != -1)
@handlers.check("__enable_response__")
@handlers.randomed_start
async def boikot(message):
    await message.reply(_("triggers.boikot"))


@dp.message_handler(lambda msg: re.search(NAKI_REGEXP, msg.text.lower()) is not None)
@handlers.check("__enable_response__")
@handlers.randomed_start
async def naki(message):
    await message.reply("Майкл Наки — в жопе козинаки")


@dp.message_handler(lambda msg: msg.text.lower().find("яблоко") != -1 or
                                msg.text.lower().find("яблочн") != -1)
@handlers.randomed_start
@handlers.check("__enable_response__")
async def apple(message):
    await message.reply(_("triggers.apple"))


@dp.message_handler(lambda msg: re.search(BAN_REGEXP, msg.text.lower()) is not None)
@handlers.check("__enable_response__")
@handlers.randomed_start
async def get_a_ban(message):
    ban_messages = _("triggers.ban_messages")
    bwords = ban_messages.get(message.from_user.id) or ban_messages["all"]

    bword = choice(bwords)

    if type(bword) == str:
        await message.reply(bword, parse_mode="HTML",
                            disable_web_page_preview=True)

    elif type(bword) == dict:
        await message.reply(bword["text"], parse_mode="HTML")
        await message.answer_sticker(bword["sticker"])

    await bot.restrict_chat_member(message.chat.id,
                                   message.from_user.id,
                                   until_date=time.time()+60)


@dp.message_handler(lambda msg: msg.text.lower().find("бот,") != -1)
@handlers.check("__enable_response__")
async def question(message):
    await message.reply(choice(["Да", "Нет"]))


@dp.message_handler(content_types=["sticker"], user_id=788415801)
async def test(message):
    if message.sticker.emoji in list("🥲😢😭😣😖😞😔😕🙁☹️😥😓😰"):
        await message.delete()
