import httpx


def say(text: str, voice: str = "aleksandr") -> str:
    r = httpx.Request("GET",
        "https://tts.chez.work/say",
        params=dict(
            text=text,
            voice=voice,
            format="opus",
            rate=55,
            pitch=10,
            volume=100
        )
    )

    return str(r.url)
