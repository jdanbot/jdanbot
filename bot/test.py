from components.token import bot
import traceback


@bot.message_handler(["987G87S98DFUS89D"])
def unpoll(message):
    pass


try:
    bot.polling(none_stop=True)

except Exception as e:
    bot.send_message("795449748",
                     f"`{str(traceback.format_exc())}`",
                     parse_mode="Markdown")
