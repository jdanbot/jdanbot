import os

import ffmpeg
from aiogram import types

from ..config import _, dp


@dp.message_handler(commands=["fast", "slow"])
async def edit_gif(message: types.Message):
    reply = message.reply_to_message

    if reply.animation:
        (video := reply.animation).file_size
    elif reply.sticker and reply.sticker.is_video:
        (video := reply.sticker).file_size
    elif reply.video:
        (video := reply.video).file_size
    else:
        raise KeyError("Reply to GIF | video | video sticker")

    if video.file_size > 5000000:
        await message.reply(_("errors.is_too_big_gif"))
        return

    await video.download(destination_file="test.mp4")
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


@dp.message_handler(commands=["reverse"])
async def reverse_gif(message: types.Message):
    reply = message.reply_to_message

    if reply.animation:
        (video := reply.animation).file_size
    elif reply.sticker and reply.sticker.is_video:
        (video := reply.sticker).file_size
    elif reply.video:
        (video := reply.video).file_size
    else:
        raise KeyError("Reply to GIF | video | video sticker")

    if video.file_size > 5000000:
        await message.reply(_("errors.is_too_big_gif"))
        return

    await video.download(destination_file="test3.mp4")

    process = (
        ffmpeg.input("test3.mp4")
        .output("test4.mp4", vf="reverse")
        .overwrite_output()
        .run_async()
    )

    process.communicate()

    await message.reply_animation(animation=open("test4.mp4", "rb"))

    os.remove("test3.mp4")
    os.remove("test4.mp4")
