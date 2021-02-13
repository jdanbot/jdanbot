# Lib is made by @apache_lenya (telegram)

from aiogram.utils import json

# символы
TAB = "  "
MIDDLE_ITEM = "├"
END_ITEM = "└"
NO_ITEM = "│"
ITEM = "─"


def iter_last(iterable):
    iterable = iter(iterable)

    try:
        p = next(iterable)
    except StopIteration:
        return False

    for i in iterable:
        yield p, False
        p = i

    yield p, True


def make_tree(d, title="root", default_line="") -> str:
    lines = list()

    lines.append(title)

    if isinstance(d, list):
        d = {str(i): val for i, val in enumerate(d)}

    for (key, val), end in iter_last(d.items()):
        if end:
            before_item = END_ITEM
        else:
            before_item = MIDDLE_ITEM

        line = default_line
        line += f"{before_item}{ITEM}"

        if isinstance(val, dict) or isinstance(val, list):
            dline = default_line
            dline += (NO_ITEM if not end else " ") + " "
            val = make_tree(val, title=key, default_line=dline)
            line += val
        else:
            line += f"{key}: {val}"
        lines.append(line)

    return "\n".join(lines)
