from .token import bot
from .lib.wikipedia import Wikipedia
import telebot
import re


digits_pattern = re.compile(r'.{,}', re.MULTILINE)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        matches = re.match(digits_pattern, query.query)

    except AttributeError as ex:
        return

    try:
        wiki = Wikipedia("ru")
        q = matches.group()
        r = wiki.search(q, 5)
        print(q)
        btns = []
        for page in r:
            p = wiki.getPage(page[0])
            img = wiki.getImageByPageName(page[0], 75)
            full_img = wiki.getImageByPageName(page[0])
            t1 = re.sub("<b>", f'<a href="{full_img}">', wiki.parsePage(p), 1)

            t2 = re.sub("</b>", "</a>", t1, 1)
            if img != -1 and full_img != -1:
                btns.append(telebot.types.InlineQueryResultArticle(
                        id=page[1], title=page[0],
                        # Описание отображается в подсказке,
                        # message_text - то, что будет отправлено в виде сообщения
                        description=p.text[:100],
                        input_message_content=telebot.types.InputTextMessageContent(
                        message_text=t2,
                        parse_mode="HTML"),
                        thumb_url=img, thumb_width=48, thumb_height=48
                ))
            else:
                btns.append(telebot.types.InlineQueryResultArticle(
                        id=page[1], title=page[0],
                        # Описание отображается в подсказке,
                        # message_text - то, что будет отправлено в виде сообщения
                        description=p.text[:100],
                        input_message_content=telebot.types.InputTextMessageContent(
                        message_text=wiki.parsePage(p),
                        parse_mode="HTML"),
                        thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/75px-Wikipedia-logo-v2.svg.png", thumb_width=48, thumb_height=48
                ))

        bot.answer_inline_query(query.id, btns)
    except Exception as e:
        print(f"{type(e)}\n{str(e)}")
