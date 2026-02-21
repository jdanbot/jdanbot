from dataclasses import dataclass

from aiogram import types
from aiogram.filters import Command, CommandObject
from pydantic import BaseModel, Field
from wikipya.exceptions import NotFound

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
    pos_title: str | None = None
    name: str = Field(alias="word")
    senses: list[Sense]
    etymology_text: str | None = None

    tags: list[str] = []
    categories: list[str] = []

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

    @property
    def article(self) -> str | None:
        if self.lang_code != "de":
            return None

        if len(self.tags) > 0:
            match self.tags[0]:
                case "feminine":
                    return "die "
                case "masculine":
                    return "der "
                case "neuter":
                    return "das "

        if len(self.categories) > 0:
            if any(
                x in self.categories
                for x in [
                    "Средний род/de",
                    "German neuter nouns",
                ]
            ):
                return "das "
            if any(
                x in self.categories
                for x in [
                    "Женский род/de",
                    "German feminine nouns",
                ]
            ):
                return "die "
            if any(
                x in self.categories
                for x in [
                    "Мужской род/de",
                    "German masculine nouns",
                ]
            ):
                return "der "


def format_list(i: str, sense: str, lang: str) -> str:
    if lang == "de":
        return f"[{i}] {sense}"

    return ". ".join([i, sense])


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


@dataclass
class Kaikki:
    lang: str

    def get_word(self, word: str) -> str:
        return "ping"


@router.message(
    Command(
        *[
            f"v{slang}{flang}"
            for slang in LANGMAP["en"]
            for flang in ("inen", "inru", "inde", "", "2")
        ]
    ),
    GetText(disable_reply=True),
)
async def wiktionary(
    message: types.Message,
    query: str,
    command: CommandObject,
):
    _ = command.command

    if _.endswith("2"):
        _ = _.removesuffix("2")
        _ = _ + "in" + _[-2:]

    langs = (
        _.removeprefix("v")
        .split(" ")[0]
        .split("2")
    )

    if len(langs) == 1:
        langs = langs[0].split("in")

    lang_raw, inlang = (
        langs[0],
        next(iter(langs[1:2]), "ru"),
    )

    results = await get_word(inlang, lang_raw, query)

    await message.reply(
        "\n\n".join(results),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


async def get_word(
    inlang: str, lang_raw: str, query: str
) -> str:
    lang = LANGMAP[inlang][lang_raw]

    res, text = await aioget(
        f"https://{DOMAINS[inlang]}/{lang}/meaning/{query[0]}/{query[0:2]}/{query}.jsonl"
    )

    if "404 Not Found" in text:
        query = query[0].swapcase() + query[1:]
        res, text = await aioget(
            f"https://{DOMAINS[inlang]}/{lang}/meaning/{query[0]}/{query[0:2]}/{query}.jsonl"
        )

        if "404 Not Found" in text:
            raise NotFound("test")

    results = []

    for line in text.strip().split("\n"):
        from msgspec import json

        json_line = json.decode(line)
        
        try:
            ipa = (
                json_line["sounds"][0]["ipa"]
                .replace("[", "/")
                .replace("]", "/")
            )
        except:
            try:
                ipa = (
                    json_line["sounds"][1]["ipa"]
                    .replace("[", "/")
                    .replace("]", "/")
                )
            except:
                ipa = ""

        try:
            if lang_raw != "en":
                raise
            
            sounds = json_line["sounds"]
            for sound in sounds:
                if "Received-Pronunciation" in sound.get("tags", []):
                    ipa = (
                        sound["ipa"]
                        .replace("[", "/")
                        .replace("]", "/")
                    )
                    break

        except:
            pass

        ipa_usa = ""
        try:
            sounds = json_line["sounds"]
            for sound in sounds:
                if "General-American" in sound.get("tags", []):
                    ipa_usa = (
                        sound["ipa"]
                        .replace("[", "/")
                        .replace("]", "/")
                    )
                    break

        except:
            ipa_usa = ""

        word = KaikkiWord.model_validate_json(line)

        all_senses = []

        for sense in word.senses:
            glos = sense.any_glosses

            if len(glos) == 2:
                glos = [f"{glos[0]} <b>{glos[1]}</b>"]

            all_senses.extend(glos)

        emoji = get_lang_emoji_by_name(word.lang_code)

        if emoji == word.lang_code:
            prefix = f" in {word.lang}"
            emoji = "🏁"
        else:
            prefix = ""

        space = (
            "\n🗣 "
            if ipa != "" and len(word.name) > 8
            else " "
        )

        if lang_raw == "en":
            common_ipa = ipa + ipa_usa

            ipa = common_ipa.replace("//", " $ ")
            #     if ipa_usa != "":
            #         ipa_usa += " (AmE)"

            end = (
                "\n"
                if ipa != "" and len(word.name) > 8
                else ""
            )
        else:
            end = ""

        results.append(
            (
                f"{emoji} <b>{word.article or ''}<a href='https://{inlang}.wiktionary.org/wiki/{query}'>{word.name}</a></b> ({word.pos_title or word.pos}){prefix}{space}{ipa}{end}\n"
                + "\n".join(
                    [
                        format_list(
                            *map(str, x), word.lang_code
                        )
                        for x in enumerate((all_senses), 1)
                    ]
                )
            ).strip()
        )

    return results
