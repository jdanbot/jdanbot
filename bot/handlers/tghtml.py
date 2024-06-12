from typing import Optional
from markdownify import markdownify as html2md
from markdown import markdown as md2html
from pyquery import PyQuery as jq

from pydantic import BaseModel, Field


def unwrap(i: int, tag: jq, space: str = "\n\n"):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with(contents + space)


def remove(i: int, tag: jq):
    jq(tag).replace_with("")


def rename(i: int, tag: jq, tag_name: str):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with((f"<{tag_name}>{contents}</{tag_name}>"))


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
        text: Optional[str] = None,
        html: Optional[str] = None,
        **kwargs,
    ) -> "TgHTML":  # type: ignore
        super(TgHTML, self).__init__(text=text or html, **kwargs)
        self.__post_init__()

    def __post_init__(self):
        # 0. clean html and filter shit
        d = jq(self.text)

        d.find("a").each(lambda i, x: unwrap(i, x, ""))

        d.find("span").filter(
            lambda i, x: jq(x).attr("style") == "font-style:italic;"
        ).each(lambda i, x: rename(i, x, "i"))
        d.find("cite").each(lambda i, x: rename(i, x, "i"))
        d.find("strong").each(lambda i, x: rename(i, x, "b"))
        d.find("blockquote blockquote").each(
            lambda i, x: unwrap(i, x, "")
        )
        d.find("p").filter(
            lambda i, p: p.text is not None
            and (
                "Это статья о" in p.text
                or "Vide etiam paginam discretivam:" in p.text
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
            *self.blocklist,
        )
        # 1. to markdown
        self.markdown = html2md(d.html(), bullets="■•")

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
            .replace("\n\n", "\n")
            # .replace("\n\n", "\n")
            # .replace("\n", "\n\n")
            .replace("<blockquote>\n", "<blockquote>")
        )

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
    def html(self) -> Optional[str]:
        return self.text
