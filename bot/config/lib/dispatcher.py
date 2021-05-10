from aiogram import Dispatcher as DispatcherBase
import i18n


class Dispatcher(DispatcherBase):
    def locale_message_handler(self, *args, **kwargs):
        def argument_wrapper(func):
            @self.message_handler(*args, **kwargs)
            async def wrapper(message):
                i18n.load_path.append("./bot/i18n")
                i18n.set("locale", message.from_user.language_code)
                i18n.set("fallback", "ru")

                return await func(message, _=i18n.t)

            return wrapper

        return argument_wrapper
