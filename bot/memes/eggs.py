from aiogram import types

from ..lib.text import code
from ..config import dp, settings
from ..lib import chez
from .. import handlers


egg_commands = []


for egg in settings.eggs:
    egg_commands.extend(egg.commands)


@dp.message_handler(commands=egg_commands)
async def sendEgg(message: types.Message):
    command = message.text.split()[0][1:]

    for egg in settings.eggs:
        if command in egg.commands:
            audio = egg.audio
            break

    await message.reply_voice(
        open(settings.music_path / audio, "rb+")
    )


@dp.message_handler(commands=["say"])
@handlers.get_text
async def say(message: types.Message, text: str):
    await message.reply_voice(
        chez.say(text)
    )


@dp.message_handler(commands=["0x00001488"])
async def secret_error(message: types.Message):
    await message.reply(
        code("A problem has been detected and KanobuOS has been shutdown to prevent damage to your computer.\n\nThe problem seems to be caused by the following file: canobu.exe\n\nSYSTEM_BAN_EXCEPTION_NOT_HANDLED\n\nIf this is the first time you've seen this stop error screen, restart your bot. If this screen appears again, follow these steps:\n\nCheck to make sure any new hardware or software is properly installed.If this is a new installation, ask your hardware or software manufacturer for any KanobuOS updates you might need.\n\nIf problems continue, disable or remove any newly installed hardware or software. Disable BAN memory options such as caching or shadowing. If you need to use safe mode to remove or disable components, restart your computer, press F to select Advanced Startup Options, and then select Safe Ban.\n\nTechnical Information:\n\n*** STOP: 0x1000007e (0xffffffffc0000005, 0xfffff80002e55151, 0xfffff880009a99d8, 0xfffff880009a9230)\n*** canobu.exe - Address 0x00001488 base at 0xfffff80002e0d000 DateStamp0x4ce7951a"),  # noqa E501a
        parse_mode="HTML"
    )
