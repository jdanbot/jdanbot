import textwrap
from typing import Union

#TODO: Full rewrite

from aiogram.utils.markdown import hcode as code, hitalic as italic, hbold as bold, quote_html as fixHTML
from aiogram.utils.parts import paginate


def prettyword(n: int, forms: Union[list, tuple, str]) -> str:
    if isinstance(forms, str):
        return forms

    if n % 100 in [11, 12, 13, 14]:
        return forms[2]

    elif n % 10 == 1:
        return forms[0]

    elif n % 10 in [2, 3, 4]:
        return forms[1]

    else:
        return forms[2]


def cute_crop(text: str, limit: int = 100) -> str:
    return paginate(text, limit=limit)


def fixWords(text: str) -> str:
    namelist = [
        ["у́", "у"],

        ["Белоруссия", "Беларусь"],
        ["Белоруссии", "Беларуси"],
        ["Беларуссию", "Беларусь"],
        ["Белоруссией", "Беларусью"],
        ["Белоруссиею", "Беларусью"],

        ["на Украин", "в Украин"],
    ]

    for name in namelist:
        text = text.replace(*name)

    return text
