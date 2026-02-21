from msgspec import json
from pydantic import BaseModel

from ...lib.aioget import aioget


class AioGoogleTranslator(BaseModel):
    from_lang: str = "auto"
    to_lang: str

    async def translate(self, query: str) -> str:
        r, text = await aioget(
            "https://clients5.google.com/translate_a/t",
            client="dict-chrome-ex",
            sl=self.from_lang,
            tl=self.to_lang,
            q=query,
        )

        return json.decode(text)[0][0]
