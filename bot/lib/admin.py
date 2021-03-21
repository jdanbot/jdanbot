async def check_admin(message, bot):
    chatid = message.chat.id
    userid = message.from_user.id

    user = await bot.get_chat_member(chatid, userid)

    return user.status == "creator" or user.status == "administrator"
