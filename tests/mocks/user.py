from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link
from pydantic import BaseModel


class UserMock(BaseModel):
    id: int = 0

    full_name: str | None = None
    url: str | None = None

    is_bot: bool = False

    first_name: str = "x"
    last_name: str = "y"
    username: str = "xy"

    def __post_init__(self) -> None:
        self.full_name = f"{self.first_name} {self.last_name}" or self.first_name
        self.url = create_tg_link("user", id=self.id)

    # @property
    # def full_name(self) -> str:
    #     if self.last_name:
    #         return f"{self.first_name} {self.last_name}"
    #     return self.first_name

    def mention_html(self, name: str | None = None) -> str:
        if name is None:
            name = self.full_name
        return markdown.hlink(name, self.url)
