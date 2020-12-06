from .token import bot, heroku
from .texts import texts


def send_meme(message, text):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id, text,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, text)


memes = {
    "bylo": "Было",
    "ne_bylo": "Не было",
    "rzaka": texts["rzaka"],
    "rzaka_full": texts["rzaka_full"],
    "rzaka_time": f"{texts['rzaka_time']} часов"
}


@bot.message_handler(commands=["bylo"])
def bylo(message):
    send_meme(message, memes["bylo"])


@bot.message_handler(commands=["ne_bylo"])
def ne_bylo(message):
    send_meme(message, memes["ne_bylo"])


@bot.message_handler(commands=["rzaka"])
def rzaka(message):
    send_meme(message, memes["rzaka"])


@bot.message_handler(commands=["rzaka_full"])
def rzaka_full(message):
    send_meme(message, memes["rzaka_full"])


@bot.message_handler(commands=["rzaka_time"])
def rzaka_time(message):
    send_meme(message, memes["rzaka_time"])


@bot.message_handler(commands=["java1"])
def java_secret(message):
    file = "bot/java.ogg" if heroku else "java.ogg"
    bot.send_voice(message.chat.id, open(file, "rb+"))


@bot.message_handler(commands=["xxx_music"])
def xxx_secret(message):
    file = "bot/music.ogg" if heroku else "music.ogg"
    bot.send_voice(message.chat.id, open(file, "rb+"))


@bot.message_handler(commands=["0x00001488"])
def secret_error(message):
    bot.reply_to(message, """<code>A problem has been detected and KanobuOS has been shutdown to prevent damage
to your computer.

The problem seems to be caused by the following file: canobu.exe

SYSTEM_BAN_EXCEPTION_NOT_HANDLED

If this is the first time you've seen this stop error screen,
restart your bot. If this screen appears again, follow
these steps:

Check to make sure any new hardware or software is properly installed.
If this is a new installation, ask your hardware or software manufacturer
for any KanobuOS updates you might need.

If problems continue, disable or remove any newly installed hardware
or software. Disable BAN memory options such as caching or shadowing.
If you need to use safe mode to remove or disable components, restart
your computer, press F to select Advanced Startup Options, and then
select Safe Ban.

Technical Information:

*** STOP: 0x1000007e (0xffffffffc0000005, 0xfffff80002e55151, 0xfffff880009a99d8,
0xfffff880009a9230)

*** canobu.exe - Address 0x00001488 base at 0xfffff80002e0d000 DateStamp
0x4ce7951a</code>""", parse_mode="HTML")


@bot.message_handler(commands=["ban"])
def ban(message):
    msg = message.text.replace("/ban@jDan734_bot", "").replace("/ban", "")
    send_meme(message, "Бан" + msg)


@bot.message_handler(commands=["fake"])
def polak(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    path = "bot/images/polak.jpg" if heroku else "../images/polak.jpg"

    try:
        bot.send_photo(message.chat.id, open(path, "rb"),
                       reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_photo(message.chat.id, open(path, "rb").read())
