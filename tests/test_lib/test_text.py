import sys
import asyncio

sys.path.insert(0, ".")

from bot.lib.text import cute_crop


class TestCuteCrop:
    def test_basic_crop(self):
        assert len(cute_crop("a" * 4096 + " t", limit=4096)) == 4096

    def test_real_crop(self):
        enter = "OS Patches metarepository"
        out = "OS Patches"

        assert cute_crop(enter, limit=20) == out
