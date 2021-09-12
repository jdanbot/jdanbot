import urllib


def say(text: str, voice: str = "aleksandr") -> str:
    host = "https://tts.chez.work/say?"
    params = dict(
        text=text, voice=voice, format="opus",
        rate=55, pitch=10, volume=100
    )

    return host + urllib.parse.urlencode(params)
