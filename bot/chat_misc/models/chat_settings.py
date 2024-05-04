from pydantic import BaseModel
from typing import Literal


class TextInput(BaseModel):
    text: str | None
    is_enabled: bool = False


class ChatSettings(BaseModel):
    class Reactions(BaseModel):
        welcome: str = ""
        rules: str = ""

        delete_joines: bool = False

        @property
        def is_enabled(self) -> bool | None:
            if self.welcome.is_enabled != self.rules.is_enabled:
                return None

            return self.welcome.is_enabled

    reactions: Reactions = Reactions()

    warns_to_ban: Literal[3, 5, -1] = 3
    language: Literal["ru", "en", "uk"] | None
