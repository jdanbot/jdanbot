import re
import json
import requests

from bs4 import BeautifulSoup


class Lurkmore:
    def __init__(self):
        self.url = "https://ipv6.lurkmo.re/api.php"
        self.params = {"format": "json", "action": "query"}

    def _get(self, params):
        self.params = {**self.params, **params}

        r = requests.get(self.url, self.params)

        if not r.status_code == 200:
            return 404

        return json.loads(r.text)

    def search(self, query, limit=1):
        """
            https://lurkmore.to/api.php?action=query&format=json&list=search&srsearch=%D0%9F%D1%83%D1%82%D0%B8%D0%BD&srprop=size&srlimit=1
        """
        r = self._get({
                "list": "search",
                "srsearch": query,
                "srprop": "size",
                "srlimit": limit
            })

        results = []

        for item in r["query"]["search"]:
            results.append(item["title"])

        return results

    def opensearch(self, query, limit=1):
        """
            https://lurkmore.to/api.php?action=opensearch&search=%D0%BF%D1%83%D1%82%D0%B8%D0%BD
        """
        r = self._get({
                "action": "opensearch",
                "search": query,
                "limit": limit
            })

        results = []

        for item in r[1]:
            results.append(item)

        return results

    def getPage(self, title):
        r = self._get({
                "action": "parse",
                "page": title,
                "prop": "text",
                "redirects": True,
                "section": 0
            })

        return r["parse"]["text"]["*"]

    def getImagesList(self, title):
        r = self._get({
                "action": "parse",
                "page": title,
                "prop": "images",
                "redirects": True,
                "section": 0
            })

        return r["parse"]["images"]

    def getImage(self, filename):
        r = self._get({
                    "search": f"Файл:{filename}"
                })

        soup = BeautifulSoup(r.text, 'lxml')

        return "https:" + soup.find("div", id="file").a.img["src"]

    def parse(self, page):
        soup = BeautifulSoup(page, 'lxml')

        for t in soup.findAll("table", {"class": "lm-plashka"}):
            t.replace_with("")

        for t in soup.findAll("table", {"class": "lm-plashka-tiny"}):
            t.replace_with("")

        for t in soup.findAll("table", {"class": "tpl-quote-tiny"}):
            t.replace_with("")

        for t in soup.findAll("div", {"class": "gallerytext"}):
            t.replace_with("")

        bold_text = []

        for tag in soup.findAll("b"):
            bold_text.append(tag.text)

        try:
            page_text = first if (first := soup.find("p").text.strip()) \
                              else soup.findAll("p", recursive=False)[1] \
                                      .text \
                                      .strip()

            page_text = page_text.replace("<", "&lt;") \
                                 .replace(">", "&gt;") \
                                 .replace(" )", ")") \
                                 .replace("  ", " ")

            for bold in bold_text:
                page_text = re.sub(bold, f"<b>{bold}</b>", page_text, 1)

        except Exception as e:
            print(e)
            return 404

        return soup
