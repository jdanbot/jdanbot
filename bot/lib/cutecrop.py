def cuteCrop(page, limit=1, text=""):
    for p in page.split("\n"):
        if len(text) + len(p) + 2 <= limit:
            text += p + "\n"
    
    return text
