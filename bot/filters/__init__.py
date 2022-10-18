from aiogram import Dispatcher
from ..config import dp


def setup(dispatcher: Dispatcher):
    from .superuser import IsSuperuserFilter
    from .admin import IsAdminFilter
    from .random import WithRandomFilter

    dispatcher.filters_factory.bind(IsSuperuserFilter)
    dispatcher.filters_factory.bind(IsAdminFilter)
    dispatcher.filters_factory.bind(WithRandomFilter)


setup(dp)
