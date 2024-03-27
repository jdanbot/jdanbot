import httpx
from pydantic import BaseModel
import aiogram
from aiogram import types
from .. import handlers
from ..lib.models import CustomField
from ..config import dp
from ..translator.crazy import get_lang_emoji_by_name

class Sense(BaseModel):
    glosses: list[str]
    raw_glosses: list[str] = None

    @property
    def any_glosses(self) -> list[str]:
        return self.raw_glosses or self.glosses


class KaikkiWord(BaseModel):
    lang: str
    lang_code: str
    pos: str
    word: str
    senses: list[Sense]
    etymology_text: str = None


    @property
    def formatted_etymology(self) -> str:
        if self.etymology_text is None:
            return ""
        
        return f"<i>{self.etymology_text}</i>"

    @property
    def lang_emoji(self) -> str:
        try:
            return get_lang_emoji_by_name(self.lang_code) + " "
        except:
            return ""

LANGMAP = {
    "en": {
        "de": "German",
        "ru": "Russian",
        "en": "English",
        "it": "Italian",
        "la": "Latin",
        "pl": "Polish",
        "uk": "Ukranian",
        "al": "All languages combined"
    },
    "ru": {
        "de": "Немецкий",
        "ru": "Русский",
        "en": "Английский",
        "it": "Итальянский",
        "la": "Латинский",
        "pl": "Польский",
        "uk": "Украинский",
        "al": "All languages combined"
    }
}

DOMAINS = {
    "en": "kaikki.org/dictionary",
    "ru": "kaikki.org/ruwiktionary"
}


@dp.message_handler(commands=[
    f"v{slang}{flang}" for slang in LANGMAP["en"]
                       for flang in ("inen", "inru", "")])
@handlers.parse_arguments_new
async def wiktionary(
    message: types.message,
    query: CustomField(str)
):
    command = message.get_command().split("@")[0].removeprefix("/v").split(" ")[0].split("2")

    if len(command) == 1:
        command = command[0].split("in")

    lang_raw, inlang = command[0], next(iter(command[1:2]), "ru")
    lang = LANGMAP[inlang][lang_raw]

    res_raw = httpx.get(f"https://{DOMAINS[inlang]}/{lang}/meaning/{query[0]}/{query[0:2]}/{query}.json")

    results = []

    for line in res_raw.text.strip().split("\n"):
        word = KaikkiWord.model_validate_json(line)

        all_senses = []

        for sense in word.senses:
            glos = sense.any_glosses

            if len(glos) == 2:
                glos = [f"{glos[0]} <b>{glos[1]}</b>"]

            all_senses.extend(glos)

        results.append((f"{word.lang_emoji}<b><a href='https://{inlang}.wiktionary.org/wiki/{query}'>{word.word}</a></b> ({word.pos}) in {word.lang}\n\n"
            + "\n".join([". ".join(map(str, x)) for x in enumerate((
            all_senses
        ), 1)])).strip())

    await message.reply(
        "\n\n".join(results),
        parse_mode="HTML",
        disable_web_page_preview=True
    )