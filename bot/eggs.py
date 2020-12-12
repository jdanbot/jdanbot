from .bot import bot, dp
from .data import data


@dp.message_handler(commands=["java1"])
async def java_secret(message):
    await bot.send_voice(message.chat.id,
                         open("music/java.ogg", "rb+"),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["cool_music"])
async def cool_secret(message):
    await bot.send_voice(message.chat.id,
                         open("music/music.ogg", "rb+"),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["0x00001488"])
async def secret_error(message):
    await message.reply("""<code>A problem has been detected and KanobuOS has been shutdown to prevent damage
to your computer.

The problem seems to be caused by the following file: canobu.exe

SYSTEM_BAN_EXCEPTION_NOT_HANDLED

If this is the first time you've seen this stop error screen,
restart your bot. If this screen appears again, follow
these steps:

Check to make sure any new hardware or software is properly installed.
If this is a new installation, ask your hardware or software manufacturer
for any KanobuOS updates you might need.

If problems continue, disable or remove any newly installed hardware
or software. Disable BAN memory options such as caching or shadowing.
If you need to use safe mode to remove or disable components, restart
your computer, press F to select Advanced Startup Options, and then
select Safe Ban.

Technical Information:

*** STOP: 0x1000007e (0xffffffffc0000005, 0xfffff80002e55151, 0xfffff880009a99d8,
0xfffff880009a9230)

*** canobu.exe - Address 0x00001488 base at 0xfffff80002e0d000 DateStamp
0x4ce7951a</code>""", parse_mode="HTML")
