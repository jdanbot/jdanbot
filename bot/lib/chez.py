from requests import Request

def say(text):
    host = "https://tts.chez.work/say"
    params = {"text": "{text}".format(text=text),
              "voice": "irina",
              "format": "opus",
              "rate": "80",
              "pitch": "80",
              "volume": "50"}

    return Request("GET", host, params=params).prepare().url
