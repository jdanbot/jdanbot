import traceback

import httpx

from pydantic import BaseModel, Field

from typing import Optional
from dataclasses import dataclass, field


CURRENCIES = {
    840: "🇺🇸",
    980: "🇺🇦",
    978: "🇪🇺",
    643: "🇷🇺",
    985: "🇵🇱"
}


def get_emoji(code: int) -> str:
    emoji = CURRENCIES.get(code)
    return emoji if emoji is not None else code


class Currency(BaseModel):
    from_currency: int = Field(alias="currencyCodeA")
    to_currency: int = Field(alias="currencyCodeB")

    date: int

    rate_cross: Optional[float] = Field(alias="rateCross")

    rate_buy: Optional[float] = Field(alias="rateBuy")
    rate_sell: Optional[float] = Field(alias="rateSell")

    @property
    def from_emoji(self) -> str:
        return get_emoji(self.from_currency)

    @property
    def to_emoji(self) -> str:
        return get_emoji(self.to_currency)


class Currencies(BaseModel):
    __root__: list[Currency]


@dataclass
class MonobankApi:
    """
    A simple async api for monobank.ua with pydantic 
    """

    _currencies: list[Currency] = field(default_factory=list)

    async def get_currencies(self) -> list[Currency]:
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get("https://api.monobank.ua/bank/currency")
                self._currencies = Currencies.parse_raw(res.text).__root__
            except:
                traceback.print_exc()

            return self._currencies
