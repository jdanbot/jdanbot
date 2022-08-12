from turtle import down
import pytest

from ..types import MessageMock
from bot.develop.wget import wget, download


def cut_lines(text: str, lines: int = -1) -> str:
    return "\n".join(text.split("\n")[:lines])


@pytest.mark.asyncio
async def test_wget_handler():
    message_mock = MessageMock(text="/r jdan734.me")

    await wget(message=message_mock)

    assert cut_lines(message_mock.replies[0].text.strip()) == """
🟢 *jdan734.me*

🔘 *Code*: 200
📦 *Size*: 4.0 KiB""".strip()


@pytest.mark.asyncio
async def test_download_handler():
    message_mock = MessageMock(text="/d jdan734.me/scss/font.scss")

    await download(message=message_mock)

    assert message_mock.replies[0].text.strip() == """
<code>@font-face {
    font-family: 'JetBrains Mono';
    font-weight: normal;
    font-style: normal;

    src: url('jbmono/JetBrainsMono-Regular.ttf');
}

@font-face {
    font-family: 'JetBrains Mono';
    font-weight: bold;
    font-style: normal;

    src: url('jbmono/JetBrainsMono-Bold.ttf');
}
</code>""".strip()
