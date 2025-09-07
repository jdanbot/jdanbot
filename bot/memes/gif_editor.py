from pathlib import Path

import ffmpeg
from aiogram import F, types
from aiogram.filters import Command, CommandObject
from shellous import sh

from ..config import Locale, bot, router


@router.message(
    F.reply_to_message,
    F.reply_to_message.animation
    | F.reply_to_message.sticker.is_video
    | F.reply_to_message.video,
    Command("fast", "slow", "reversed", "to_gif"),
)
async def edit_gif(
    message: types.Message,
    command: CommandObject,
    _: Locale,
):
    reply: types.Message = message.reply_to_message
    video: (
        types.Animation | types.Sticker | types.Video | None
    ) = reply.animation or reply.sticker or reply.video

    if video.file_size > 500_000_00:
        await message.reply(_.errors.too_big_gif)
        return

    _in = Path("/tmp/TEST.mp4")
    out = Path("/tmp/TEST2.mp4")

    await bot.download(video, _in.absolute())
    is_fast = command.command == "fast"

    process = ffmpeg.input(str(_in))

    if command.command in ("fast", "slow"):
        process = process.filter(
            "setpts", "0.25*PTS" if is_fast else "1.25*PTS"
        )

    if command.command == "reversed":
        process = process.output(str(out), vf="reverse")
    else:
        process = process.output(str(out))

    await sh(process.compile())
    await message.reply_animation(
        animation=types.FSInputFile(path=out)
    )

    _in.unlink()
    out.unlink()


@router.message(
    F.reply_to_message,
    Command("fast", "slow", "reversed", "to_gif"),
)
async def edit_gif_without_source(message: types.Message):
    await message.reply("you only replied")


@router.message(
    Command("fast", "slow", "reversed", "to_gif"),
)
async def edit_gif_without_source_and_reply(
    message: types.Message,
):
    await message.reply("you only send command")
