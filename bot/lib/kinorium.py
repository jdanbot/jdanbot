from dataclasses import dataclass
from typing import Literal

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

try:
    from aioget import aioget
except:
    from .aioget import aioget

import aiohttp
from pydantic import BaseModel, Field

ua = UserAgent()


@dataclass
class ReelScaryRatings:
    total: float
    gore: float
    disturb: float
    suspense: float


@dataclass
class ParentControlProperty:
    label: str
    severity_label: str

    @property
    def severity(self) -> Literal[1, 2, 3]:
        match self.severity_label:
            case "мало" | "few":
                return 1
            case "середньо" | "средне" | "average":
                return 2
            case "багато" | "много" | "plenty":
                return 3

    @property
    def severity_emoji(self) -> Literal["🟢", "🟡", "🔴"]:
        return ["🟢", "🟡", "🔴"][self.severity - 1]

    @property
    def type(self) -> Literal[0, 1, 2, 3, 4]:
        match self.label:
            case "лякаючі сцени" | "пугающие сцены" | "Frightening & Intense Scenes":
                return 0
            case "жорстокість/кров" | "жестокость/кровь" | "Violence & Gore":
                return 1
            case "секс/нагота" | "Sex & Nude":
                return 2
            case "алкоголь, наркотики, куріння" | "алкоголь, наркотики, курение" | "Alcohol, Drugs & Smoking":
                return 3
            case "ненормативна лексика" | "ненормативная лексика" | "Profanity":
                return 4

    @property
    def type_emoji(self) -> str:
        return ["👻", "🩸", "🔞", "🚬", "🤬"][self.type]


class MovieRatings(BaseModel):
    friends: str | None
    imdb: str
    kinorium: str
    kinopoisk: str | None

    critics: str


@dataclass
class Movie:
    name: str
    original_name: str

    published_at: int
    countries: list[str]

    duration: str

    parent_control: list[ParentControlProperty]
    # parent_control: tuple[Literal[0, 1, 2, 3]] = tuple([0, 0, 0, 0])

    genres: list[str]

    rating: MovieRatings

    poster: str
    description: str | None

    # reelscary_rating: ReelScaryRatings = ReelScaryRatings(0, 0, 0, 0)

    @property
    def parent_control_tuple(self) -> tuple[Literal[1, 2, 3]]:
        return tuple(map(lambda x: x.severity, self.parent_control))

    @property
    def horror_criteria(self) -> float:
        return round(sum(self.parent_control_tuple) * (10 - self.rating.kinorium), 2)

    @property
    def horror_criteria_label(self) -> str:
        x = self.horror_criteria

        if x < 20:
            return "low"
        if x > 20 and x < 50:
            return "normal"
        if x > 50 and x < 80:
            return "hard"
        if x > 80 and x < 90:
            return "nightmare"
        if x > 90:
            return "ultra nightmare"


class MovieStatus(BaseModel):
    id: str
    title: str


class MoviePreview(BaseModel):
    id: int
    name: str
    name_orig: str
    year: int | None | str = None
    mixtype: str
    poster: str | None
    is_serial: bool | None = Field(alias="isSerial")

    begin: int | None = Field(alias="year_serial_b")
    end: int | None = Field(alias="year_serial_e")

    show_status: MovieStatus | None

    class RatingData(BaseModel):
        class Rating(BaseModel):
            rating: float | str

        kr: Rating

    ratingData: RatingData

    @property
    def rating(self) -> float | None:
        try:
            return float(self.ratingData.kr.rating)
        except ValueError:
            return None


class KinoriumSearchResults(BaseModel):
    __root__: list[MoviePreview]


class MovieSitePreview(BaseModel):
    id: int
    year: str | None
    poster: str | None

    name: str
    original_name: str | None

    genres: list[str]
    countries: list[str]


@dataclass
class Kinorium:
    lang: Literal["en", "uk", "ru"] = "uk"

    @staticmethod
    async def search(query: str) -> list[MovieSitePreview]:
        cookies = {
        }

        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(
                "https://uk.kinorium.com/search/",
                params=dict(q=query),
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                },
            ) as resp:
                text = await resp.text()

        soup = BeautifulSoup(text, "html.parser")

        return [
            MovieSitePreview(
                id=film.find("h3")["data-id"],
                name=film.find("h3").text.strip(),
                year=(small := film.find("small")).text.split(",")[0].strip(),
                original_name=small_text[1].strip()
                if len(small_text := small.text.split(",")) > 1
                else None,
                poster=None
                if (poster := film.find("img")) is None
                or poster["src"].endswith(".svg")
                else poster["src"],
                genres=film.find(class_="search-page__genre-list")
                .text.strip()
                .split(", "),
                countries=film.find(class_="search-page__genre-list")
                .next_sibling.text.strip()
                .split(", "),
            )
            for film in soup.find(class_="movieList").find_all(class_="item")
        ]

    @staticmethod
    async def get(movie_id: int) -> Movie:
        cookies = {
        }

        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(
                f"https://uk.kinorium.com/{movie_id}/",
                headers={
                    "user-agent": ua.random,
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                }
            ) as resp:
                text = await resp.text()

        soup = BeautifulSoup(text, "html.parser")

        return Movie(
            name=soup.find("h1", class_="film-page__title-text").text,
            original_name=soup.find("span", itemprop="alternativeHeadline").text,
            duration=(
                soup.find("table", class_="infotable")
                .find_all("tr")[1]
                .find("td", class_="data")
                .text.strip()
            ),
            countries=[
                country.text
                for country in soup.find(class_="film-page__country-links").find_all(
                    "a"
                )
            ],
            published_at=int(soup.find(class_="film-page__date").find("a").text),
            parent_control=[
                (ParentControlProperty(
                    label=severity.contents[0].strip(),
                    severity_label=severity.find("p").text,
                )
                for severity in soup.find(class_="parentalguide")
                .find("ul")
                .find_all("li"))] if soup.find(class_="parentalguide") else [],
            genres=[
                genre.a.text
                for genre in soup.find("ul", class_="genres").find_all(
                    "li", itemprop="genre"
                )
            ],
            rating=MovieRatings(
                friends=None,
                imdb=(
                    soup.find("a", class_="ratingsBlockIMDb")
                    .find("span", class_="value")
                    .text.strip()
                ),
                kinorium=(
                    soup.find("ul", class_="ratingsBlock")
                    .find_all("li")[1]
                    .find("span", class_="value")
                    .text.strip()
                ),
                kinopoisk=(
                    soup.find("a", class_="ratingsBlockKP")
                    .find("span", class_="value")
                    .text.strip()
                ),
                critics=(
                    soup.find("ul", class_="ratingsBlock")
                    .find_all("li")[-1]
                    .find("span", class_="value")
                    .text.strip().removesuffix("%")
                ),
            ),
            poster=soup.find_all(class_="movie_gallery_item")[0].get("data-photo"),
            description=page_text.text.strip()
            .split(" ", maxsplit=1)[1] if (page_text := soup.find(class_="film-page__text")) else None,
        )


async def main():
    films = await Kinorium.search("жах на")

    from pprint import pprint

    for film in films:
        pprint(film.__dict__)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
