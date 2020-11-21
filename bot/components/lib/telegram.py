class Telegram:
    def __init__(self, bot):
        self.bot = bot

    def photo(self, message):
        try:
            self.file_id = message.reply_to_message.photo[-1].file_id
        except:
            self.file_id = message.reply_to_message.document.thumb.file_id

        return [self.file_id, self.bot.get_file(self.file_id)]

    def parse(self, message, len_=2):
        commands = message.text.split(" ")
        if len(commands) == len_:
            return commands
        else:
            return 404

    def delete_message(self, message):
        try:
            self.bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
