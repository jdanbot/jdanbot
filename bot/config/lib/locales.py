import re
from typing import Any

import toml
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from pytils import numeral
from rich import print


def fix_russian(count: int, variants: str):
    variants = variants.replace(",", "/,").replace("|", ",")

    return numeral.get_plural(count, variants)


class Template(str):
    def __call__(self, *args, **kwargs) -> str:
        tmpl = self
        tmpl = self[:]
        tmpl = re.sub(
            r"\[(\w+):([^\]]+)\]",
            lambda x: fix_russian(
                int(
                    kwargs[
                        (
                            y := x.group(0)[1:-1].split(
                                ":", maxsplit=1
                            )
                        )[0]
                    ]
                ),
                y[1],
            ),
            tmpl,
        )

        return tmpl.format(**kwargs)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls, handler(str)
        )


class Locale(BaseModel):
    cases: list[str]

    class Pidor(BaseModel):
        top_10: str
        works_only_in_chats: str
        total_members: Template

        reg: str
        in_db: str
        already_in_db: str

        pidor_left: str
        already_finded: list[Template]
        pidor_searching: list[list[str]]
        today_pidor: list[Template]

    pidor: Pidor

    class Notes(BaseModel):
        create_var: Template
        enter_note_name: str

        add_note: str
        edit_note: str

        not_found: str
        successful_deleted: str

    notes: Notes

    class Templates(BaseModel):
        about_user: Template
        stats: Template
        status: Template
        wget: Template

    templates: Templates

    class Errors(BaseModel):
        enter_wiki_query: str
        few_args: Template

        only_vars: str
        not_found: str
        template: str

        too_big_gif: str
        failed_to_recognize: str

        class CommandRequires(BaseModel):
            reply: str
            text: str
            reply_or_text: str

        command_requires: CommandRequires

    errors: Errors

    docs: dict[str, str]


class Locales(BaseModel):
    ru: Locale
    # en: Locale


toml_file = toml.load("locales/ru.toml")
locales = Locales(ru=toml_file)


# print(locales)
# print(locales.ru.pidor.reg)
