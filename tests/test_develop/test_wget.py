import pytest

from ..mocks import MessageMock
from ..lib import cut_lines
from bot.develop.wget import wget, download


@pytest.mark.asyncio
async def test_wget_handler():
    await wget(message_mock := MessageMock("/r jdan734.me"))
    assert (
        cut_lines(message_mock.replies[0].text)
        == (
            "🟢 *jdan734.me*\n\n"  # noqa
            "🔘 *Code*: 200\n"     # noqa
            "📦 *Size*: 4.0 KiB"   # noqa
        )
    )


@pytest.mark.asyncio
async def test_download_handler():
    await download(message_mock := MessageMock(text="/d jdan734.me/scss/font.scss"))

    assert (
        message_mock.replies[0].text
        == (
            "<code>@font-face {\n"
            "    font-family: 'JetBrains Mono';\n"
            "    font-weight: normal;\n"
            "    font-style: normal;\n\n"
            "    src: url('jbmono/JetBrainsMono-Regular.ttf');\n"
            "}\n\n"
            "@font-face {\n"
            "    font-family: 'JetBrains Mono';\n"
            "    font-weight: bold;\n"
            "    font-style: normal;\n\n"
            "    src: url('jbmono/JetBrainsMono-Bold.ttf');\n"
            "}\n"
            "</code>"
        )
    )
