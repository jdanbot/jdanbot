from ..config import bot, Note, IMAGE_PATH, _

from .admin import check_admin
from .photo import Photo


def parse_arguments(limit, without_params=False):
    def argument_wrapper(func):
        async def wrapper(message):
            params = message.text.split(maxsplit=limit - 1)

            if len(params) < limit and not without_params:
                await message.reply(_("errors.few_args", num=limit),
                                    parse_mode="Markdown")
            else:
                await func(message, params)

        return wrapper

    return argument_wrapper


def check(var, without_params=False):
    def argument_wrapper(func):
        async def wrapper(message):
            res = Note.get(message.chat.id, var)

            if res is None:
                res = "True"

            if str(res).title() == "True":
                await func(message)

        return wrapper

    return argument_wrapper


def get_reply_photo(func):
    async def wrapper(message, params):
        reply = message.reply_to_message
        file_id = ""

        if reply:
            if reply.photo:
                file_id = reply.photo[-1].file_id
            elif reply.document:
                file_id = reply.document.thumb.file_id
        else:
            await message.reply(_("errors.reply_photo"))
            return

        photo = await bot.get_file(file_id)
        file = await bot.download_file(photo.file_path)

        await func(message, params, [file_id, file])

    return wrapper


def init_photo_file(func):
    @get_reply_photo
    async def wrapper(message, params, photo):
        path = IMAGE_PATH.format(image=photo[0])

        with open(path, "wb") as new_file:
            new_file.write(photo[1].read())

        img = Photo(path)
        await func(message, params, img)

    return wrapper


def get_text(func):
    @parse_arguments(2, without_params=True)
    async def wrapper(message, params):
        reply = message.reply_to_message

        if reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        elif len(params) == 2:
            text = params[1]
        else:
            await message.reply(_("errors.few_args", num=1),
                                parse_mode="Markdown")
            return

        await func(message, text)

    return wrapper


def only_jdan(func):
    async def wrapper(message):
        if message.from_user.id == 795449748:
            await func(message)

    return wrapper


def only_admins(func):
    async def wrapper(message):
        if message.chat.type == "supergroup" and \
           await check_admin(message, bot):
            await func(message)

    return wrapper
