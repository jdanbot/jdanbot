from aiovk import TokenSession, API

from .config import ACCESS_TOKEN
from .lib.driver import HttpDriver


session = TokenSession(access_token=ACCESS_TOKEN, driver=HttpDriver())
vk_api = API(session)
