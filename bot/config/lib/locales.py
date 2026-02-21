import re
from typing import Any

from msgspec import Struct, toml

from ...lib.text import prettyword


class Template(str):
    def __call__(self, **kwargs) -> str:
        return self.format(**kwargs)

    def format(self, **kwargs) -> str:
        def replace_plural(match):
            key, forms = match.group(1), match.group(2)
            count = kwargs.get(key, 0)
            forms_list = forms.split("|")

            if len(forms_list) == 3:
                return " ".join(
                    [
                        str(count),
                        prettyword(count, forms_list),
                    ]
                )
            return count + " " + match.group(0)

        result = re.sub(
            r"\[(\w+):([^\]]+)\]", replace_plural, self
        )
        return result.format(**kwargs)


class Locale(Struct, frozen=True):
    cases: set[str]

    class Pidor(Struct, frozen=True):
        top_10: str
        works_only_in_chats: str
        total_members: Template

        reg: str
        in_db: str
        already_in_db: str

        pidor_left: str
        already_finded: list[Template]
        pidor_searching: list[frozenset[str]]
        today_pidor: list[Template]

    pidor: Pidor

    class Notes(Struct, frozen=True):
        create_var: Template
        enter_note_name: str

        add_note: str
        edit_note: str

        not_found: str
        successful_deleted: str

    notes: Notes

    class Templates(Struct, frozen=True):
        about_user: Template
        stats: Template
        status: Template
        wget: Template

    templates: Templates

    class Errors(Struct, frozen=True):
        enter_wiki_query: str
        few_args: Template

        only_vars: str
        not_found: str
        template: str

        too_big_gif: str
        failed_to_recognize: str

        class CommandRequires(Struct, frozen=True):
            reply: str
            text: str
            reply_or_text: str

        command_requires: CommandRequires

    errors: Errors

    docs: dict[str, str]


class Locales(Struct):
    ru: Locale
    # en: Locale


def dec_hook(type: type, o: Any) -> Template:
    if type is Template:
        return Template(o)

    raise NotImplementedError(
        f"Objects of type {type(o)} are not supported."
    )


with open("locales/ru.toml") as file:
    locales = Locales(
        ru=toml.decode(
            file.read(), type=Locale, dec_hook=dec_hook
        ),
    )
