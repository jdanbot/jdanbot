import json
import requests


def getRules(page):
    r = requests.get(f"https://api.telegra.ph/getPage/{page}")
    rules = json.loads(r.text)["result"]
    return rules
