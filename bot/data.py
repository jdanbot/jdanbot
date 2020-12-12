import yaml

with open("bot/data.yml", encoding="UTF-8") as file:
    data = yaml.safe_load(file.read())
