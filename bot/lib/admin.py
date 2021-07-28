async def check_admin(message, bot):
    chatid = message.chat.id
    userid = message.from_user.id

    user = await bot.get_chat_member(chatid, userid)

    return user.status == "creator" or user.status == "administrator"


def get_tag(admin):
    if admin.username:
        return f"@{admin.username}"
    else:
        return f"<a href='{admin.url}'>{admin.first_name}</a>"