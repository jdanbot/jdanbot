import yaml


with open("bot/triggers/legacy_triggers.yml") as f:
    triggers = yaml.safe_load(f.read())
