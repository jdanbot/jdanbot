import yaml

from os import environ


class Config:
    def __init__(self, file_path="config.yml"):
        try:
            with open(file_path, encoding="UTF-8") as file:
                self.config = yaml.full_load(file.read())
        except Exception:
            self.config = {}

        self.environ = environ

    def get(self, param, default=None):
        globals()[param.upper()] = self.config.get(param) or \
                                   self.environ.get(param.upper()) or \
                                   default


config = Config()
config.get("db_path", default="jdanbot.db")
config.get("delay", default=30)
config.get("rss_feeds", default=[])
config.get("rss", default=False)
config.get("image_path", default="bot/cache/{image}.jpg")
config.get("token")
config.get("status", default="unknown")
config.get("vk", default=False)
config.get("youtube", default=False)
config.get("vk_channels")
config.get("access_token")
