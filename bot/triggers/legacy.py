from msgspec import toml

with open("bot/triggers/legacy_triggers.toml") as file:
    triggers = toml.decode(file.read())
