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

    return '\n\n'.join(clean_text)
