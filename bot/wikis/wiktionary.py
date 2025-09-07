from aiogram import types
from aiogram.filters import Command, CommandObject
from pydantic import BaseModel, Field

from ..config.bot import router
from ..filters import GetText
from ..lib.aioget import aioget
from ..translator.crazy import get_lang_emoji_by_name


class Sense(BaseModel):
    glosses: list[str]
    raw_glosses: list[str] | None = None

    @property
    def any_glosses(self) -> list[str]:
        return self.raw_glosses or self.glosses


class KaikkiWord(BaseModel):
    lang: str
    lang_code: str
    pos: str
    name: str = Field(alias="word")
    senses: list[Sense]
    etymology_text: str | None = None

    @property
    def formatted_etymology(self) -> str:
        if self.etymology_text is None:
            return ""

        return f"<i>{self.etymology_text}</i>"

    @property
    def lang_emoji(self) -> str:
        try:
            return (
                get_lang_emoji_by_name(self.lang_code) + " "
            )
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
        "al": "All languages combined",
    },
    "ru": {
        "de": "Немецкий",
        "ru": "Русский",
        "en": "Английский",
        "it": "Итальянский",
        "la": "Латинский",
        "pl": "Польский",
        "uk": "Украинский",
        "al": "All languages combined",
    },
    "de": {
        "de": "Deutsch",
        "ru": "Russisch",
        "en": "Englisch",
        "it": "Italienisch",
        "la": "Latein",
        "pl": "Polnisch",
        "uk": "Ukrainisch",
        "al": "All languages combined",
    },
}

DOMAINS = {
    "en": "kaikki.org/dictionary",
    "ru": "kaikki.org/ruwiktionary",
    "de": "kaikki.org/dewiktionary",
}


@router.message(
    Command(
        *[
            f"v{slang}{flang}"
            for slang in LANGMAP["en"]
            for flang in ("inen", "inru", "inde", "")
        ]
    ),
    GetText(disable_reply=True),
)
async def wiktionary(
    message: types.Message,
    query: str,
    command: CommandObject,
):
    langs = (
        command.command.removeprefix("v")
        .split(" ")[0]
        .split("2")
    )

    if len(langs) == 1:
        langs = langs[0].split("in")

    lang_raw, inlang = (
        langs[0],
        next(iter(langs[1:2]), "ru"),
    )
    lang = LANGMAP[inlang][lang_raw]

    res_raw = await aioget(
        f"https://{DOMAINS[inlang]}/{lang}/meaning/{query[0]}/{query[0:2]}/{query}.jsonl"
    )

    results = []

    for line in res_raw.text.strip().split("\n"):
        word = KaikkiWord.model_validate_json(line)

        all_senses = []

        for sense in word.senses:
            glos = sense.any_glosses

            if len(glos) == 2:
                glos = [f"{glos[0]} <b>{glos[1]}</b>"]

            all_senses.extend(glos)

        results.append(
            (
                f"{word.lang_emoji}<b><a href='https://{inlang}.wiktionary.org/wiki/{query}'>{word.name}</a></b> ({word.pos}) in {word.lang}\n\n"
                + "\n".join(
                    [
                        ". ".join(map(str, x))
                        for x in enumerate((all_senses), 1)
                    ]
                )
            ).strip()
        )

    await message.reply(
        "\n\n".join(results),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
