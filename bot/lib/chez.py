from requests import Request

def say(text):
    host = "https://tts.chez.work/say"
    params = {"text": "{text}".format(text=text),
              "voice": "aleksandr",
              "format": "opus",
              "rate": "55",
              "pitch": "10",
              "volume": "70"}

    return Request("GET", host, params=params).prepare().url
