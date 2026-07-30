from aiogram import types
from aiogram.filters import Command
from msgspec import Struct
from selectolax.lexbor import LexborHTMLParser

from ..config import router
from ..filters import GetText
from ..lib.aioget import aioget


class Package(Struct, frozen=True):
    distro: str
    version: str
    is_actual: bool


class Project(Struct, frozen=True):
    name: str
    packages: list

    latest_version: str


async def get_project(query: str = "inori") -> Project:
    __, text = await aioget(
        f"https://repology.org/badge/vertical-allrepos/{query}.svg"
    )
    svg = LexborHTMLParser(text).css_first("svg")

    packages = []

    for g in svg.css('g[font-size="11"]'):
        pkg = Package(
            distro=g.css_first("text").text(),
            version=g.css_first(
                'text[text-anchor="middle"]'
            ).text(),
            is_actual=g.prev.prev.attributes["fill"]
            == "#4c1",
        )

        packages.append(pkg)

    return Project(
        name=query, packages=packages, latest_version=""
    )


DISTROS = {
    "OpenBSD Ports": "🐡 OpenBSD",
    "Alpine Linux 3.24": "🏔 Alpine Linux 3.24",
    "AUR": "📦 AUR",
    "Arch Linux": "🅰️ Arch Linux",
    "Void Linux x86_64": "🟢 Void Linux",
    "Termux": "🤖 Termux",
    "Ubuntu 26.04": "♻️ Ubuntu 26.04",
    "Artix": "🌌 Artix",
    "Debian 14": "🌀 Debian 14",
    "pkgsrc-2026Q2": "🚩 NetBSD",
    "FreeBSD Ports": "👹 FreeBSD",
    "nixpkgs stable 26.05": "❄️ NixOS",
}


@router.message(Command("pkg", "repology"), GetText())
async def get_weather_func(
    message: types.Message, query: str
):
    pkg = await get_project(query)
    variants = filter(
        lambda x: x.distro in DISTROS.keys(),
        pkg.packages,
    )

    msg = f"📦 *{query.capitalize()} Versions*\n\n"

    for v in variants:
        for distro in DISTROS.keys():
            if v.distro == distro:
                msg += f"*{DISTROS[distro]}*: {v.version}\n"

    await message.reply(msg, parse_mode="Markdown")
