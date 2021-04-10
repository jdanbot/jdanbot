import yaml
import aiohttp

from tghtml import TgHTML
from bs4 import BeautifulSoup
from aiogram.utils import json

with open("bot/lib/blocklist.yml") as file:
    blocklist = yaml.safe_load(file.read())


class Lurkmore:
    def __init__(self):
        self.url = "https://ipv6.lurkmo.re/api.php"
        self.url2 = "https://ipv6.lurkmo.re"
        self.params = {"format": "json", "action": "query"}

    async def _get(self, params):
        self.params = {"format": "json", "action": "query"}
        self.params = {**self.params, **params}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as response:
                if not response.status == 200:
                    return 404

                return json.loads(await response.text())

    async def search(self, query, limit=1):
        """
            https://lurkmore.to/api.php?action=query&format=json&list=search&srsearch=%D0%9F%D1%83%D1%82%D0%B8%D0%BD&srprop=size&srlimit=1
        """
        r = await self._get({
                "list": "search",
                "srsearch": query,
                "srprop": "size",
                "srlimit": limit
            })

        results = []

        for item in r["query"]["search"]:
            results.append(item["title"])

        return results

    async def opensearch(self, query, limit=1):
        """
            https://lurkmore.to/api.php?action=opensearch&search=%D0%BF%D1%83%D1%82%D0%B8%D0%BD
        """
        r = await self._get({
                "action": "opensearch",
                "search": query,
                "limit": limit
            })

        return r

    async def getPage(self, title):
        r = await self._get({
                "action": "parse",
                "page": title,
                "prop": "text",
                "redirects": "true",
                "section": 0
            })

        return r["parse"]["text"]["*"]

    async def getImagesList(self, title):
        r = await self._get({
                "action": "parse",
                "page": title,
                "prop": "images",
                "redirects": "true",
                "section": 0
            })

        images_list = []

        for item in r["parse"]["images"]:
            if item not in blocklist["images"]:
                images_list.append(item)

        return images_list

    def getImageFromFandomPage(self, page):
        p = BeautifulSoup(page, "lxml")

        try:
            for t in p.find("aside").findAll("h2"):
                t.replace_with("")
        except Exception:
            pass

        try:
            i = p.find("aside").find("a", {"class": "image"})

            return i["href"]
        except Exception:
            return 404

    async def getImage(self, filename, host=""):
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"{self.url2}/File:{filename}")

            if not response.status == 200:
                return 404

            text = await response.text()
            soup = BeautifulSoup(text, 'lxml')

            return "https:" + host + soup.find("div", id="file").a.img["src"]

    def findImagesInPage(self, imagelist, div):
        url_list = []

        for img in div.find_all("img"):
            if img["src"].find("/skins/") != -1:
                pass
            elif img["src"] in blocklist["images_in_page"]:
                pass
            else:
                url_list.append("https:" + img["src"])
        return url_list

    def parse(self, page):
        arch_class = "archwiki-template-meta-related-articles-start"

        return TgHTML(page, [
            ["table", {"class": "lm-plashka"}],
            ["table", {"class": "lm-plashka-tiny"}],
            ["table", {"class": "tpl-quote-tiny"}],
            ["div", {"class": "thumbinner"}],
            ["div", {"class": "gallerytext"}],
            ["aside"],
            ["table"],
            ["div", {"class": arch_class}],
            ["div", {"class": "noprint"}],
            ["span", {"id": "w4g_rb_area-1"}]
        ]).parsed
