from yarl import URL


def say(text: str, voice: str = "aleksandr") -> str:
    r = URL("https://tts.chez.work/say")

    return r.with_query(
        text=text,
        voice=voice,
        format="opus",
        rate=55,
        pitch=10,
        volume=100,
    ).__str__()
