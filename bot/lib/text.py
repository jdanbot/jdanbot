import textwrap
from typing import Union


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


def cuteCrop(text: str, limit: int = 100) -> str:
    return (textwrap.shorten(text.replace("\n", "<br>"), limit, placeholder="")
                    .replace("<br>", "\n")
                    .replace("• ", "<b>• </b>"))


def code(text: str) -> str:
    return f"<code>{fixHTML(text)}</code>"


def bold(text: str) -> str:
    return f"<b>{fixHTML(text)}</b>"


def italic(text: str) -> str:
    return f"<i>{fixHTML(text)}</i>"


def fixHTML(text: str) -> str:
    return (str(text).replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;"))


def fixWords(text: str) -> str:
    namelist = [
        ["у́", "у"]

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
