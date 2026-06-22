from pathlib import Path

from aiogram import F, types
from aiogram.filters import Command, CommandObject
from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg
from msgspec import json

from ..config import Locale, bot, router

FFMPEG_PIXEL_MAGIC = (
    "scale=iw/8:ih/8,scale=8*iw:8*ih:flags=neighbor"
)
FFMPEG_BAD_AUDIO = "compand=attacks=0.01:decays=0.1:points=-80/-80|-30/-20|-10/0|0/0, equalizer=f=3000:t=q:w=2:g=-20, volume=10"


@router.message(
    F.reply_to_message,
    F.reply_to_message.animation
    | F.reply_to_message.sticker.is_video
    | F.reply_to_message.video,
    Command(
        "fast",
        "slow",
        "reverse",
        "reversed",
        "to_gif",
        "p4",
        "p8",
        "p14",
    ),
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

    video_name = getattr(
        video,
        "file_name",
        getattr(video, "file_unique_id", "test"),
    ).__str__()
    file = Path("/tmp") / f"test-{video_name}.mp4"
    output = Path("/tmp") / f"{video_name}_edit.mp4"

    await bot.download(video, file)

    match command.command:
        case "fast":
            params = dict(
                vf="setpts=0.5*PTS",
                af="atempo=2.0",
            )
        case "slow":
            params = dict(
                vf="setpts=2.0*PTS",
                af="atempo=0.5",
            )
        case "reverse" | "reversed":
            params = dict(
                vf="reverse",
                af="areverse",
            )
        case "to_gif":
            params = dict(an=None)
        case "p4":
            params = dict(
                vf=FFMPEG_PIXEL_MAGIC.format(p="4"),
                af=FFMPEG_BAD_AUDIO,
                ab="1k",
            )
        case "p8":
            params = dict(
                vf=FFMPEG_PIXEL_MAGIC.format(p="8"),
                af=FFMPEG_BAD_AUDIO,
                ab="4k",
            )
        case "p14":
            params = dict(
                vf=FFMPEG_PIXEL_MAGIC.format(p="14"),
                af=FFMPEG_BAD_AUDIO,
                ab="8k",
            )
        case _:
            params = dict()

    ffprobe = FFmpeg(executable="ffprobe").input(
        str(file),
        print_format="json",
        show_entries="stream=nb_read_frames",
        count_frames=None,
        select_streams="v:0",
    )

    media = json.decode(await ffprobe.execute())
    total_frames = int(
        media["streams"][0]["nb_read_frames"]
    )

    ffmpeg = FFmpeg().input(file).output(output, **params)

    @ffmpeg.on("stderr")
    def on_stderr(line):
        print("stderr:", line)

    global i
    i = 0

    global msg
    msg = await message.reply(
        "We started!", parse_mode=None
    )

    @ffmpeg.on("progress")
    async def on_progress(progress: Progress):
        global i
        global msg

        if i != 0:
            i -= 1
            return

        percent = 100 * (progress.frame / total_frames)

        await msg.edit_text(
            f"<b>{int(percent)}%</b> {progress.frame} / {total_frames} | {progress.time}",
            parse_mode="html",
        )

        i = 3

    @ffmpeg.on("completed")
    async def on_completed():
        global msg
        await msg.delete()

    await ffmpeg.execute()

    await bot.send_chat_action(
        message.chat.id, "upload_video"
    )
    await message.reply_animation(
        animation=types.FSInputFile(path=output)
    )

    file.unlink()
    output.unlink()


@router.message(
    F.reply_to_message,
    Command(
        "fast", "slow", "reversed", "reverse", "to_gif"
    ),
)
async def edit_gif_without_source(message: types.Message):
    await message.reply("you only replied")


@router.message(
    Command(
        "fast", "slow", "reversed", "reverse", "to_gif"
    ),
)
async def edit_gif_without_source_and_reply(
    message: types.Message,
):
    await message.reply("you only send command")
