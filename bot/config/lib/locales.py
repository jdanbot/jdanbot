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
    lang: str
    cases: list[str]

    class Pidor(Struct, frozen=True):
        top_10: str
        works_only_in_chats: str
        total_members: Template

        reg: str
        in_db: str
        already_in_db: str
        stats_unavailable: str

        pidor_left: str
        already_finded: list[Template]
        pidor_searching: list[list[str]]
        today_pidor: list[Template]

    pidor: Pidor

    class Notes(Struct, frozen=True):
        create_var: Template
        enter_note_name: str

        add_note: str
        edit_note: str

        not_found: str
        successful_deleted: str

        no_notes: str

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

    class Ban(Struct, frozen=True):
        selfmute: Template
        mute: Template
        unmute: Template
        warn: Template
        unwarn: Template
        kick: Template
        warn_limit_reached: Template
        reason_not_found: str
        admin_cant_unwarn_self: str
        warns_not_found: str
        selfmute_limit_reached: str

    ban: Ban

    docs: dict[str, str]

    class Settings(Struct, frozen=True):
        reactions: str
        warns_to_ban: str
        locale: str
        done: str

        button_back: str

        settings_text: str
        language_text: str
        warns_to_ban_text: str

    settings: Settings

    class Menu(Struct, frozen=True):
        main: str
        network: str
        wiki: str
        ffmpeg: str
        admin: str
        system: str
        notes: str
        pidor: str

        class MenuButtons(Struct, frozen=True):
            main: str
            network: str
            wiki: str
            ffmpeg: str
            admin: str
            system: str
            notes: str
            pidor: str

        buttons: MenuButtons

    menu: Menu

    class Modules(Struct, frozen=True):
        description: str
        admin: str

        mute: str
        warn: str

        selfmute: str
        polls: str

    modules: Modules


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
