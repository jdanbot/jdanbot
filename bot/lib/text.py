def prettyword(n, forms):
    if n % 100 in [11, 12, 13, 14]:
        return forms[2]

    elif n % 10 == 1:
        return forms[0]

    elif n % 10 in [2, 3, 4]:
        return forms[1]

    else:
        return forms[2]


def cuteCrop(page, limit=1, text=""):
    for p in page.split("\n"):
        if len(text) + len(p) + 2 <= limit:
            text += p + "\n"

    clean_text = []
    text_splited = text.split("\n")

    for p in text_splited:
        if p == "":
            pass
        else:
            clean_text.append(p)

    return "\n\n".join(clean_text)


def code(text):
    return f"<code>{fixHTML(text)}</code>"


def bold(text):
    return f"<b>{fixHTML(text)}</b>"


def fixHTML(text):
    """replaces html-markup parts on tags"""
    return str(text).replace("&", "&amp;") \
                    .replace("<", "&lt;") \
                    .replace(">", "&gt;")


def fixWords(text):
    namelist = [
        ["Белоруссия", "Беларусь"],
        ["Белоруссии", "Беларуси"],
        ["Беларуссию", "Беларусь"],
        ["Белоруссией", "Беларусью"],
        ["Белоруссиею", "Беларусью"],

        ["Белору́ссия", "Белару́сь"],
        ["Белору́ссии", "Белару́си"],
        ["Белору́ссию", "Белару́сь"],
        ["Белору́ссией", "Белару́сью"],
        ["Белору́ссиею", "Белару́сью"],


        ["на Украин", "в Украин"],
    ]

    for name in namelist:
        text = text.replace(*name)

    return text
