import logging

from rich.logging import RichHandler

from .lib.filters import NoRunningJobFilter

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_path=False,
            show_level=True,
            markup=True,
        )
    ],
)
logger = logging.getLogger(__name__)

logging.getLogger("schedule").addFilter(
    NoRunningJobFilter()
)
