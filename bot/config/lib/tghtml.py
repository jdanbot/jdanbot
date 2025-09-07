from markdown import markdown as md2html
from markdownify import markdownify as html2md
from pydantic import BaseModel, Field
from pyquery import PyQuery as jq


def unwrap(i: int, tag: jq, space: str = "\n\n"):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with(contents + space)


def remove(i: int, tag: jq):
    jq(tag).replace_with("")


def deh2scrt(i: int, tag: jq):
    if tag.text is None:
        return

    jq(tag).replace_with(
        f"<b>{jq(tag).text()}HEADEREND</b>"
    )


def rename(i: int, tag: jq, tag_name: str):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with(
            (f"<{tag_name}>{contents}</{tag_name}>")
        )


def remove_hidden_elements(i: int, tag: jq):
    if (
        tag.attrib.get("style", "").replace(" ", "")
        == "display:none;"
    ):
        remove(i, tag)


class TgHTML(BaseModel):
    text: str
    output: str | None = None
    markdown: str | None = None

    blocklist: set = {}
    ALLOWED_TAGS: tuple | set = Field(
        default=(
            "b",
            "strong",
            "i",
            "em",
            "code",
            "s",
            "strike",
            "del",
            "u",
            "pre",
            "blockquote",
        ),
        serialization_alias="allowed_tags",
    )

    is_wikipedia: bool = True
    enable_preprocess: bool = True

    def __init__(
        self,
        text: str | None = None,
        html: str | None = None,
        **kwargs,
    ) -> "TgHTML":  # type: ignore
        super(TgHTML, self).__init__(
            text=text or html, **kwargs
        )
        self.__post_init__()

    def __post_init__(self):
        # 0. clean html and filter shit
        d = jq(self.text.replace("<cite>", "<cite>\n— "))

        d.find("span").filter(
            lambda i, x: jq(x).attr("style")
            == "font-style:italic;"
        ).each(lambda i, x: rename(i, x, "i"))
        d.find("span.mw-headline").each(deh2scrt)
        d.find("h2").each(lambda i, x: rename(i, x, "p"))
        d.find("cite").each(lambda i, x: rename(i, x, "i"))
        d.find("strong").each(
            lambda i, x: rename(i, x, "b")
        )
        d.find("blockquote blockquote").each(
            lambda i, x: unwrap(i, x, "")
        )
        d.find("b").filter(
            lambda i, p: p.text is not None
            and p.text == ("Избранная статья")
        ).each(remove)
        d.find("*").each(remove_hidden_elements)
        d.find("p").filter(
            lambda i, p: p.text is not None
            and (
                "Это статья о" in p.text
                or "Vide etiam paginam discretivam:"
                in p.text
            )
        ).each(remove)
        d.find("head").each(remove)
        d.find("div").filter(
            lambda i, p: p.text is not None
            and (
                p.text.startswith(
                    "Эта статья является избранной."
                )
            )
        ).each(remove)

        d.find("i").filter(
            lambda i, p: p.text is not None
            and p.text.startswith(
                "Вся обновлённая информация была взята"
            )
        ).each(remove)

        self.bulk_remove(
            d,
            "div.navigation-not-searchable",
            "table",
            "aside",
            ".error",
            ".noprint",
            "audio",
            ".thumb",
            "span.error",
            "span.mw-ext-cite-error",
            "p.hatnote",
            "figure",
            "sup.reference a",
            "span.mw-editsection-bracket",
            "div.mw-table-of-contents-container",
            "div.vector-dropdown-content",
            "title",
            "head",
            *self.blocklist,
        )

        d.find("a").each(lambda i, x: unwrap(i, x, ""))

        source = (
            str(d.html())
            .replace("<i>", "ITALICRESERVEDSIGN")
            .replace("</i>", "ITALICRESERVEDSIGN")
        )

        # 1. to markdown
        self.markdown = html2md(
            source,
            bullets="■•",
        )

        self.markdown = self.markdown.replace(
            "ITALICRESERVEDSIGN", "_"
        )

        # 2. make some markdown features ignorable
        #    in next step
        # self.md = self.md.replace("\n* ", "\n■ ")

        # 3. to html
        html = md2html(self.markdown)  # type: ignore
        tag = jq(html)

        # 4. remove default html shit like as p and div
        tag.find("div").each(lambda i, x: unwrap(i, x, ""))
        tag.find("p").each(unwrap)

        tag.find("*").filter(
            lambda i, x: x.tag not in self.ALLOWED_TAGS
        ).each(remove)

        # 5. shitcodded fixes in the end
        self.output = (
            str(tag.html())
            .replace("HEADEREND</strong>\n\n", "</strong>")
            .replace("\n\n", "\n")
            # .replace("\n\n", "\n")
            # .replace("\n", "\n\n")
            .replace("<blockquote>\n", "<blockquote>")
            .replace("\n</blockquote>", "</blockquote>")
            .replace("■", "■ ")
        ).strip()

    def bulk_remove(self, d: jq, *selectors):
        for sel in selectors:
            d.find(sel).each(remove)

    def __str__(self) -> str:
        return self.output or ""

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def parsed(self) -> str:
        return self.output or ""

    @property
    def html(self) -> str | None:
        return self.text
