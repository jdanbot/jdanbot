import imageio.v3 as iio
import os

from aiogram import types
from ..config import dp
import ffmpeg


def get_video_fps(path: str) -> int:
    """Source: https://www.codegrepper.com/code-examples/python/python+ffmpeg+get+video+fps"""

    probe = ffmpeg.probe(path)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')

    return int(video_info['r_frame_rate'].split('/')[0])


@dp.message_handler(commands=["fast", "slow"])
async def speed_up_gif(message: types.Message):
    if not hasattr(message, "reply_to_message") or not hasattr(message.reply_to_message, "animation"):
        return

    is_fast = message.get_command(pure=True) == "fast"
    fps_diff = 30 if is_fast else -30

    await message.reply_to_message.animation.download(destination_file="test.mp4")
    gif = iio.imread("test.mp4")

    fps = get_video_fps("test.mp4")

    if not is_fast and fps <= 30:
        fps_diff = 0

    iio.imwrite("test2.mp4", gif, fps=fps + fps_diff)

    with open("test2.mp4", "rb") as video:
        await message.reply_animation(animation=video)

    os.remove("test.mp4")
    os.remove("test2.mp4")
