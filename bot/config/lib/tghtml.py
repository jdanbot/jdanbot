import bleach
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


def rename(i: int, tag: jq, tag_name: str, extra: str = ""):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with(
            (f"<{tag_name}>{contents}{extra}</{tag_name}>")
        )


def replace_with_its_text(i: int, tag: jq):
    jq(tag).replace_with(jq(tag).text())


def unpack_ipa_from_span(i: int, tag: jq):
    parents = jq(tag).parents()

    for parent in parents:
        if jq(parent).is_("span.navigation-not-searchable"):
            return replace_with_its_text(i, parent)


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

        d = jq(
            self.text.replace("<cite>", "<cite>\n— ")
            .replace("&nbsp;", " ")
        )

        d(".navigation-not-searchable").each(remove)

        d(".mwe-math-element").each(
            lambda i, x: jq(x).replace_with(
                "<code>"
                + jq(x)
                .find("annotation")
                .text()
                .replace("\displaystyle ", "")
                .removeprefix("{")
                .removesuffix("}")
                .strip()
                + "</code>"
            )
        )

        d("span[style*='font-style:italic']").each(
            lambda i, x: rename(i, x, "i")
        )
        d("span.mw-headline").each(deh2scrt)
        d("h2").each(lambda i, x: rename(i, x, "p"))
        d("cite").each(lambda i, x: rename(i, x, "i"))
        d("strong").each(lambda i, x: rename(i, x, "b"))
        d("blockquote blockquote").each(
            lambda i, x: unwrap(i, x, "")
        )
        d("b").filter(
            lambda i, p: p.text is not None
            and p.text == ("Избранная статья")
        ).each(remove)
        d(".IPA").each(unpack_ipa_from_span)
        d(".IPA").each(replace_with_its_text)
        d("*").each(remove_hidden_elements)
        d("p").filter(
            lambda i, p: p.text is not None
            and (
                "Это статья о" in p.text
                or "Vide etiam paginam discretivam:"
                in p.text
            )
        ).each(remove)
        d("head").each(remove)
        d("div").filter(
            lambda i, p: p.text is not None
            and (
                p.text.startswith(
                    "Эта статья является избранной."
                )
            )
        ).each(remove)

        d("i").filter(
            lambda i, p: p.text is not None
            and p.text.startswith(
                "Вся обновлённая информация была взята"
            )
        ).each(remove)

        d(".mw-heading").each(
            lambda i, x: rename(
                i, x, "b", extra="HEADEREND"
            )
        )

        self.bulk_remove(
            d,
            "span.navigation-not-searchable",
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
            ".mbox-text",
            "dl",
            ".references",
            "style",
            "script",
            ".ext-phonos",
            *self.blocklist,
        )

        d("li").each(
            lambda i, x: d(x).replace_with(
                "■ " + d(x).html()
            )
        )

        d("a").each(lambda i, x: unwrap(i, x, ""))
        # 1. sanitaze html

        self.output = bleach.clean(
            str(d.html()),
            tags=self.ALLOWED_TAGS,
            strip=True,
        )

        self.output = (
            self.output.replace(
                "HEADEREND</b>\n\n", "</b>\n"
            )
            # .replace("\n\n", "\n")
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
            .replace("<b>\n", "<b>")
            .replace("  ", " ")
            .replace(" )", ')')
            .replace("( ", "(")
            .replace(" ; ", "; ")
            # .replace("\n", "\n\n")
            .replace("<blockquote>\n", "<blockquote>")
            .replace("\n</blockquote>", "</blockquote>")
            .replace("■", "■ ")
            .replace("■  ", "■ ")
        ).strip()

    def bulk_remove(self, d: jq, *selectors):
        for sel in selectors:
            d(sel).each(remove)

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
