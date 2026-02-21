from typing import Iterable

# TODO: Full rewrite


def prettyword(
    n: int,
    forms: list[str] | tuple[str, str, str] | str,
) -> str:
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


def paginate(
    data: Iterable, page: int = 0, limit: int = 10
) -> Iterable:
    """
    FROM AIOGRAM2

    Slice data over pages

    :param data: any iterable object
    :type data: :obj:`typing.Iterable`
    :param page: number of page
    :type page: :obj:`int`
    :param limit: items per page
    :type limit: :obj:`int`
    :return: sliced object
    :rtype: :obj:`typing.Iterable`
    """
    return data[page * limit : page * limit + limit]


def cute_crop(text: str, limit: int = 100) -> str:
    return paginate(text, limit=limit)


def fix_words(text: str) -> str:
    namelist = [
        ["у́", "у"],
        ["на Украин", "в Украин"],
    ]

    for name in namelist:
        text = text.replace(*name)

    return text
