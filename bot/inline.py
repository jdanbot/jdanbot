from .config import bot, dp, WIKIPYA_BLOCKLIST
from .lib.text import code, bold
from .locale import locale

from aiogram.types import InputTextMessageContent, \
                          InlineQueryResultAudio, InlineQueryResultArticle
from wikipya.aiowiki import Wikipya, NotFound
from bs4 import BeautifulSoup
from random import randint, choice

from .lib import chez


WIKIPEDIA_LANGS = ['aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'ar', 'as', 'av', 'ay', 'az', 'ba', 'be', 'bg', 'bh', 'bi', 'bm', 'bn', 'bo', 'br', 'bs', 'ca', 'ce', 'ch', 'co', 'cr', 'cs', 'cu', 'cv', 'cy', 'da', 'de', 'dv', 'dz', 'ee', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'ff', 'fi', 'fj', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'gv', 'gv', 'ha', 'he', 'hi', 'ho', 'hr', 'ht', 'hu', 'hy', 'hz', 'ia', 'id', 'ie', 'ig', 'ii', 'ii', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'ka', 'kg', 'ki', 'kj', 'kk', 'kl', 'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'ku', 'kv', 'kw', 'ky', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'mg', 'mh', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'my', 'na', 'nb', 'nd', 'ne', 'ng', 'nl', 'nn', 'no', 'nr', 'nv', 'ny', 'oc', 'oj', 'om', 'or', 'os', 'pa', 'pi', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sa', 'sd', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'ss', 'ss', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'wo', 'xh', 'yi', 'yo', 'za', 'zh', 'zu']


@dp.inline_handler(lambda query: True and
                   query.query.startswith("w") and
                   len(query.query.split(maxsplit=1)) == 2)
async def query_text(query):
    params = query.query.split(maxsplit=1)

    q = params[1]
    lang = params[0].split(":", maxsplit=1)
    lang = "ru" if len(lang) == 0 else lang[1]

    if not (lang in WIKIPEDIA_LANGS):
        return

    wiki = Wikipya(lang)

    try:
        search = await wiki.search(q, 3)
    except Exception as e:
        print(e)
        await bot.answer_inline_query(query.id, [
            InlineQueryResultArticle(
                id=0,
                title="При выполнении запроса возникла ошибка",
                description=e,
                input_message_content=InputTextMessageContent(
                    message_text=bold("При выполнении запроса возникла ошибка:") +
                                 code(e),
                    parse_mode="HTML"
                )
            )
        ])

        return

    buttons = []
    for item in search:
        page = await wiki.page(item)
        page.blockList = WIKIPYA_BLOCKLIST
        soup = BeautifulSoup(page.text, "lxml")
        text = page.fixed

        btn_defaults = {"id": page.pageid, "title": page.title,
                        "description": soup.text[:100],
                        "thumb_width": 48, "thumb_height": 48,
                        "input_message_content": InputTextMessageContent(
                            message_text=text,
                            parse_mode="HTML"
                        )}

        try:
            img = await page.image(75)
            buttons.append(InlineQueryResultArticle(**btn_defaults,
                                                    thumb_url=img.source))

        except NotFound:
            default_image = locale.default_wiki_image
            buttons.append(InlineQueryResultArticle(**btn_defaults,
                                                    thumb_url=default_image))

    await bot.answer_inline_query(query.id, buttons)


@dp.inline_handler(lambda query: len(query.query) == 0)
async def cock(query):
    cock_size = randint(0, 46)

    if cock_size == 46:
        cock_size = 1488

    person = choice(locale.persons)

    await bot.answer_inline_query(query.id, [
        InlineQueryResultArticle(
            id=4,
            title="Озвучить текст",
            description="Для использования введите @jdan734_bot <запрос>",
            input_message_content=InputTextMessageContent(
                message_text="Мне нечего озвучивать. Введи текст"
            )
        ),

        InlineQueryResultArticle(
            id=5,
            title="Найти в Википедии",
            description="Для использования введите @jdan734_bot wiki <запрос>",
            input_message_content=InputTextMessageContent(
                message_text="Мне нечего находить. Введи запрос"
            )
        ),

        InlineQueryResultArticle(
            id=6,
            title="Вычислить cock size",
            description="Новая иновационная система вычисляет длину члена"
                        " очень точно. Достаточно приложить хуй к экрану",
            input_message_content=InputTextMessageContent(
                message_text=f"🏳️‍🌈 Размер моего хуя *{cock_size}см*",
                parse_mode="Markdown"
            )
        ),

        InlineQueryResultArticle(
            id=7,
            title="Кто я из Профсоюза?",
            description="Определяет кто вы в профсоюзе. Точность 100%",
            input_message_content=InputTextMessageContent(
                message_text=f"В профсоюзе я *{person['name']}*\n\n"
                             f"__{person['description']}__",
                parse_mode="Markdown"
            )
        )
    ], cache_time=1)


@dp.inline_handler(lambda query: len(query.query) > 0)
async def query_say(query):
    query.query = query.query.strip()

    if query.query.endswith(".") or \
       query.query.endswith("?") or \
       query.query.endswith("!"):
        btns = [
            InlineQueryResultAudio(
                id=1, 
                title=query.query[:-1],
                audio_url=chez.say(query.query)
            )
        ]

        await bot.answer_inline_query(query.id, btns)
    else:
        btns = [
            InlineQueryResultArticle(
                id=1,
                title="Поставь точку в конце!",
                description="Надо. Вставь.",
                input_message_content=InputTextMessageContent(
                    message_text="ПРОСТО ВСТАВЬ ТОЧКУ."
                )
            )
        ]

        await bot.answer_inline_query(query.id, btns)
