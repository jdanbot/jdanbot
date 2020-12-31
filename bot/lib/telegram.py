class Telegram:
    def __init__(self, bot):
        self.bot = bot

    async def photo(self, message):
        try:
            self.file_id = message.reply_to_message.photo[-1].file_id
        except:
            self.file_id = message.reply_to_message.document.thumb.file_id

        file = await self.bot.get_file(self.file_id)

        return [self.file_id, file]

    def parse(self, message, len_=2):
        commands = message.text.split(" ")
        if len(commands) == len_:
            return commands
        else:
            return 404

    async def delete_message(self, message):
        try:
            await message.delete()
        except:
            pass
