from .token import bot
import math
import re


@bot.message_handler(commands=["sqrt"])
def sqrt(message):
    try:
        num = float(message.text.split()[1])
        res = math.sqrt(num)

        try:
            res = float(res)

        except:
            res = int(res)

        bot.reply_to(message, f"`{res}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"`{e}`", parse_mode="Markdown")


@bot.message_handler(commands=["eval", "calc"])
def calc_eval(message):
    return
    if len(str(message.text).split(maxsplit=1)) == 1:
        bot.reply_to(message, "Введи запрос для вычисления")
        return

    op = message.text.split(maxsplit=1)[1].replace(" ", "") \
                                          .replace("pi", str(math.pi)) \
                                          .replace("e", str(math.e))

    if re.search(r"[а-яА-ЯёЁa-zA-Z]", op):
        bot.reply_to(message, "Необходимая переменная не найдена")
        return

    try:
        result = eval(op)

        if int(result) == float(result):
            text = int(result)
        else:
            text = float(result)

    except ZeroDivisionError:
        text = "Деление на ноль"

    except Exception as e:
        text = f"Некорректный запрос\n{e}"

    bot.reply_to(message, f"`{str(text)}`", parse_mode="Markdown")
