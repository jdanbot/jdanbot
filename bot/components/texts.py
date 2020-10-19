import yaml

with open("texts.yml", encoding="UTF-8") as file:
    texts = yaml.safe_load(file.read())
