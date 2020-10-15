from .token import bot
from .lib.wikipedia import Wikipedia
from . import texts


def wikiSearch(message, lang="ru", logs=False):
    if len(message.text.split(maxsplit=1)) != 2:
        bot.reply_to(message, f"Пожалуйста, напишите название статьи\nНапример так: `{message.text.split(maxsplit=1)[0]} Название Статьи`", parse_mode="Markdown")
        return

    query = message.text.split(maxsplit=1)[1]
    print(f"[Wikipedia Search {lang.upper()}] {query}")

    wiki = Wikipedia(lang)

    r = wiki.search(query, 20)

    if r == -1:
        bot.reply_to(message, "Ничего не найдено")
        return

    text = ""

    for prop in r:
        text += f"{prop[0]}\n"
        text += f"└─/w_{prop[1]}\n"

    bot.reply_to(message, text)


def getWiki(message=None, lang="ru", logs=False, title=None):
    wiki = Wikipedia(lang)

    if title is None:
        if len(message.text.split(maxsplit=1)) != 2:
            bot.reply_to(message, f"Пожалуйста, напишите название статьи\nНапример так: `{message.text.split(maxsplit=1)[0]} Название Статьи`", parse_mode="Markdown")
            return

        query = message.text.split(maxsplit=1)[1]
        print(f"[Wikipedia {lang.upper()}] {query}")

        s = wiki.search(query, 1)

        if s == -1:
            bot.reply_to(message, "Ничего не найдено")
            return

        title = s[0][0]

    page = wiki.getPage(title)

    if page == -1:
        text = ""

    elif str(page) == "":
        text = ""

    else:
        for span in page.find_all("span"):
            span.name = "p"

        for p in page.find_all("p"):
            if p.text == "":
                p.replace_with("")

        text = wiki.parsePage(page)

    image = wiki.getImageByPageName(title)

    if type(image) is int:
        bot.send_chat_action(message.chat.id, "typing")
        try:
            bot.reply_to(message, text, parse_mode="HTML")

        except:
            bot.send_message(795449748, text)
            bot.reply_to(message, "Не удалось отправить статью")

    else:
        if image == "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png":
            image = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"

        bot.send_chat_action(message.chat.id, "upload_photo")
        try:
            bot.send_photo(message.chat.id,
                           image,
                           caption=text,
                           parse_mode="HTML",
                           reply_to_message_id=message.message_id)
        except:
            bot.reply_to(message, "Не удалось отправить статью")


@bot.message_handler(commands=["sru", "s", "search"])
def wikiru(message):
    wikiSearch(message, "ru")


@bot.message_handler(commands=["wikiru", "wikiru2", "wru", "w"])
def wikiru(message):
    getWiki(message, "ru")


@bot.message_handler(commands=["wikien", "van", "wen", "v"])
def wikien(message):
    getWiki(message, "en")


@bot.message_handler(commands=["wikisv", "wsv"])
def wikisv(message):
    getWiki(message, "sv")


@bot.message_handler(commands=["wikide", "wde"])
def wikide(message):
    getWiki(message, "de")


@bot.message_handler(commands=["wikice", "wce"])
def wikice(message):
    getWiki(message, "ce")


@bot.message_handler(commands=["wikitt", "wtt"])
def wikitt(message):
    getWiki(message, "tt")


@bot.message_handler(commands=["wikiba", "wba"])
def wikiba(message):
    getWiki(message, "ba")


@bot.message_handler(commands=["wikipl", "wpl"])
def wikipl(message):
    getWiki(message, "pl")


@bot.message_handler(commands=["wikiua", "wikiuk", "wuk", "wua", "pawuk"])
def wikiua(message):
    getWiki(message, "uk")


@bot.message_handler(commands=["wikibe",
                               "wbe",
                               "tarakanwiki",
                               "lukaswiki",
                               "potato",
                               "potatowiki"])
def wikibe(message):
    getWiki(message, "be")


@bot.message_handler(commands=["wikies", "wes"])
def wikies(message):
    getWiki(message, "es")


@bot.message_handler(commands=["wikihe", "whe"])
def wikihe(message):
    getWiki(message, "he")


@bot.message_handler(commands=["wikixh", "wxh"])
def wikixh(message):
    getWiki(message, "xh")


@bot.message_handler(commands=["wikiab", "wab"])
def wikiab(message):
    getWiki(message, "ab")


@bot.message_handler(commands=["wikibe-tarask", "wikibet", "wbet", "xbet"])
def wikibet(message):
    getWiki(message, "be-tarask")


@bot.message_handler(commands=["wiki_usage", "wiki2", "wiki"])
def wiki_usage(message):
    bot.reply_to(message, texts.langs, parse_mode="Markdown")


@bot.message_handler(commands=["langs", "wikilangs", "wiki_langs"])
def wiki_langs(message):
    bot.reply_to(message,
                 texts.langs_list,
                 parse_mode="Markdown",
                 disable_web_page_preview=True)
