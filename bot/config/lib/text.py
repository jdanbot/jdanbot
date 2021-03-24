def code(text):
    return f"<code>{fixHTML(text)}</code>"


def bold(text):
    return f"<b>{fixHTML(text)}</b>"


def fixHTML(text):
    """replaces html-markup parts on tags"""
    return str(text).replace("&", "&amp;") \
                    .replace("<", "&lt;") \
                    .replace(">", "&gt;")
