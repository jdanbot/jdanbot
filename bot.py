import telebot

with open("./token.txt") as token:
	bot = telebot.TeleBot(token.read())
	
@bot.message_handler(commands=["ban"])
def ban(message):
	bot.send_message(message.chat.id, "Бан")
