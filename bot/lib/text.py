from random import choice


TAG_SCHEMA = "<{tag}>{text}</{tag}>"


def prettyword(n, forms):
    if n % 100 in [11, 12, 13, 14]:
        return forms[2]

    elif n % 10 == 1:
        return forms[0]

    elif n % 10 in [2, 3, 4]:
        return forms[1]

    else:
        return forms[2]


def cuteCrop(lines, limit=100, text=""):
    lines = lines.split("\n")

    for i, line in enumerate(lines):
        back_line = lines[i - 1 if i != 0 else i]
        next_line = lines[i + 1 if i != len(lines) - 1 else i]

        is_list = line.startswith("• ")
        is_next_list = next_line.startswith("• ")

        if len(text + line) <= limit and (back_line != "" or line != ""):
            text += line + "\n"

        if len(text) + 2 <= limit and (is_list and not is_next_list and
                                       next_line != ""):
           text += "\n"
    
    return text.replace("• ", "<b>•</b> ")


def code(text):
    return f"<code>{fixHTML(text)}</code>"


def bold(text):
    return f"<b>{fixHTML(text)}</b>"


def italic(text):
    return f"<i>{fixHTML(text)}</i>"


def fixHTML(text):
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
