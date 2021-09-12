import sys
import asyncio

sys.path.insert(0, ".")

from bot.lib.text import cuteCrop


class TestCuteCrop:
    def test_basic_crop(self):
        assert len(cuteCrop("a" * 4096 + " t", limit=4096)) == 4096

    def test_real_crop(self):
        enter = "OS Patches metarepository"
        out = "OS Patches"

        assert cuteCrop(enter, limit=20) == out
