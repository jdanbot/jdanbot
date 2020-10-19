from .token import heroku
import yaml

path = "bot/texts.yml" if heroku else "texts.yml"

with open(path, encoding="UTF-8") as file:
    texts = yaml.safe_load(file.read())
