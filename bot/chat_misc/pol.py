import itertools
import re
from pathlib import Path
from typing import Iterable

from aiogram import types
from aiogram.filters import Command, CommandObject
from msgspec import toml

from ..config import router
from ..filters import GetText


def generate_word_variants_with_uppercase(
    word: str, combinations: list[str] | None = None
):
    if combinations is None:
        combinations = get_word_variants_based_on_word_len(word)

    a = list(map(itertools.permutations, combinations))

    uppercase_map = set([x for a in list(a) for x in a])
    variants = []

    for m in uppercase_map:
        variants.append(
            "".join(
                [
                    letter.upper() if int(m[i]) == 1 else letter
                    for i, letter in enumerate(word)
                ]
            )
        )

    return variants


def get_word_variants_based_on_word_len(
    word: str,
) -> Iterable[list[str]]:
    variants = [
        [1],
        [10, 11],
        [100, 110, 111],
        [1000, 1100, 1110, 1111],
    ]

    if len(word) > len(variants):
        return []

    return map(lambda x: list(str(x)), variants[len(word) - 1])


def load_polish_cyrillic_variant(path: str):
    schemas = toml.decode(Path(path).open().read()).items()
    uppercase_schemas = []

    for schema in schemas:
        pol, rus = schema

        prefix = "^" if pol.startswith("^") else ""
        pol = pol.removeprefix("^")
        end = re.match("\\w*", pol).end()
        pol, suffix = pol[:end], pol[end:]

        variants = generate_word_variants_with_uppercase(pol)

        uppercase_schemas.extend(
            list(
                map(
                    lambda x: (prefix + x, rus.capitalize() + suffix),
                    variants,
                )
            )
        )

    uppercase_schemas.extend(schemas)
    return uppercase_schemas


POLISH_EXP_TRANSLITERATION_SCHEMAS = load_polish_cyrillic_variant(
    "bot/chat_misc/lib/polish_cyr_exp.toml"
)
POLISH_TRAD_TRANSLITERATION_SCHEMAS = load_polish_cyrillic_variant(
    "bot/chat_misc/lib/polish_cyr_trad.toml"
)


@router.message(Command("cyr", "cyr2"), GetText())
async def cyr(
    message: types.Message, query: str, command: CommandObject
):
    schemas = (
        POLISH_EXP_TRANSLITERATION_SCHEMAS
        if command.command == "cyr"
        else POLISH_TRAD_TRANSLITERATION_SCHEMAS
    )

    for schema in schemas:
        query = re.sub(*schema, query)

    await message.reply(query, parse_mode=None)
