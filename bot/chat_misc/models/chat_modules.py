from pydantic import BaseModel


class ChatModules(BaseModel):
    is_admin_enabled: bool = True
    is_selfmute_enabled: bool = True
    is_poll_enabled: bool = True

    is_memes_enabled: bool = True
    is_ban_enabled: bool = True
