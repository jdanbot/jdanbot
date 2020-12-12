import requests
# import re
from bs4 import BeautifulSoup


class Habr:
    def __init__(self):
        self.url = "https://habr.com/ru/post/"

    def page(self, id_):
        r = requests.get(f"{self.url}{id_}/")
        soup = BeautifulSoup(r.text, "lxml")
        page = ""

        page += f'<b>{soup.find("h1").span.text.upper()}</b>\n\n'
        page += soup.findAll("div", {"id": "post-content-body"})[0].text

        for tag in soup.findAll("div", {"id": "post-content-body"})[0].findAll("h2"):
            page = page.replace(tag.text, f"\n<b>{tag.text}</b>")

        for tag in soup.findAll("div", {"id": "post-content-body"})[0].findAll("h3"):
            page = page.replace(tag.text, f"\n<b>{tag.text}</b>")
        # page += str(soup.findAll("div", {"id": "post-content-body"})[0]) \
        #             .replace("</div>", "") \
        #             .replace("<blockquote>", "") \
        #             .replace("</blockquote>", "") \
        #             .replace("<br/>", "\n")

        # page = re.sub(r'(\<div(/?[^>]+)>)', '', page)

        return page
