import os

import ffmpeg
from aiogram import types

from ..config import _, dp


@dp.message_handler(commands=["fast", "slow"])
async def edit_gif(message: types.Message):
    if not hasattr(message, "reply_to_message") or not hasattr(
        message.reply_to_message, "animation"
    ):
        return

    if (animation := message.reply_to_message.animation).file_size > 5000000:
        await message.reply(_("errors.is_too_big_gif"))
        return

    await animation.download(destination_file="test.mp4")
    is_fast = message.get_command(pure=True) == "fast"

    process = (
        ffmpeg.input("test.mp4")
        .filter("setpts", "0.25*PTS" if is_fast else "1.25*PTS")
        .output("test2.mp4")
        .overwrite_output()
        .run_async()
    )

    process.communicate()

    await message.reply_animation(animation=open("test2.mp4", "rb"))

    os.remove("test.mp4")
    os.remove("test2.mp4")
