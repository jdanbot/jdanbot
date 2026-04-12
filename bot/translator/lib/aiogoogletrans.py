from msgspec import Struct, json

from ...lib.aioget import aioget


class AioGoogleTranslator(Struct, frozen=True, kw_only=True):
    from_lang: str = "auto"
    to_lang: str = "auto"

    async def translate(self, query: str) -> str:
        r, text = await aioget(
            "https://clients5.google.com/translate_a/t",
            client="dict-chrome-ex",
            sl=self.from_lang,
            tl=self.to_lang,
            q=query,
        )

        answer = json.decode(text)

        if isinstance(answer[0], str):
            return answer[0]
        else:
            return answer[0][0]
