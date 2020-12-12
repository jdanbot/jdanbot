from .fixHTML import fixHTML


def code(text):
    return f"<code>{fixHTML(text)}</code>"


def bold(text):
    return f"<b>{fixHTML(text)}</b>"


def italic(text):
    return f"<i>{fixHTML(text)}</i>"
