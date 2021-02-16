import yaml
import json


class Dict2Class:
    """Dict => Class"""
    def __init__(self, dict_):
        self.add(dict_)

    def add(self, dict_):
        self._dict = dict_
        vars(self).update(dict_)


with open("bot/data.yml", encoding="UTF-8") as file:
    data = yaml.safe_load(file.read())
    data = json.loads(json.dumps(data), object_hook=Dict2Class)
