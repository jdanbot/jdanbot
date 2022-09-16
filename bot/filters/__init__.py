from aiogram import Dispatcher
from ..config import dp
# from loguru import logger

# from aiogram_bot.filters.chat_property import ChatPropertyFilter


def setup(dispatcher: Dispatcher):
    # from .has_permissions import BotHasPermissions, HasPermissions
    # from .is_reply import IsReplyFilter
    from .superuser import IsSuperuserFilter
    from .admin import IsAdminFilter
    from .random import WithRandomFilter

    text_messages = [
        dispatcher.message_handlers,
        dispatcher.edited_message_handlers,
        dispatcher.channel_post_handlers,
        dispatcher.edited_channel_post_handlers,
    ]

    # dispatcher.filters_factory.bind(IsReplyFilter, event_handlers=text_messages)
    # dispatcher.filters_factory.bind(HasPermissions, event_handlers=text_messages)
    # dispatcher.filters_factory.bind(BotHasPermissions, event_handlers=text_messages)
    # dispatcher.filters_factory.bind(ChatPropertyFilter, event_handlers=text_messages)
    dispatcher.filters_factory.bind(IsSuperuserFilter)
    dispatcher.filters_factory.bind(IsAdminFilter)
    dispatcher.filters_factory.bind(WithRandomFilter)


setup(dp)
