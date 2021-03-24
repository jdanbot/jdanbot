import yaml

import json
from os import listdir


class Dict2Class:
    """Dict => Class"""
    def __init__(self, dict_):
        self.add(dict_)

    def add(self, dict_):
        try:
            vars(self).update(dict_)
        except:
            pass

        for item in dict_:
            if type(item).__name__ == "list":
                return Dict2Class(item)

            elif type(dict_[item]).__name__ == "dict":
                self.__dict__[item] = Dict2Class(dict_[item])


LOCALE_PATH = "bot/locale"
files = listdir(LOCALE_PATH)

locale = json.loads("{}", object_hook=Dict2Class)

for _ in files:
    if not _.endswith(".yml"):
        continue

    with open(f'{LOCALE_PATH}/{_}', encoding="UTF-8") as file:
        locale.add(yaml.safe_load(file.read()))

# with open("bot/data.yml", encoding="UTF-8") as file:
#     data = yaml.safe_load(file.read())
#     data = json.loads(json.dumps(data), object_hook=Dict2Class)
