import inspect
import logging
import sys

from loguru import logger as loggr

try:
    from rich.console import Console
    from rich.traceback import Traceback

    RICH_ENABLED = True

    import io
except ModuleNotFoundError:
    import traceback

    RICH_ENABLED = False

FORMAT_ = "<d>|</d>".join(
    [
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green>",
        "<level>{level:5}</level>",
        "<blue>{name}</blue>:<yellow>{line}</yellow>",
        "<level>{message}</level>\n",
    ]
)


def rich_formatter(record):
    """
    Original code: https://github.com/Delgan/loguru/issues/540#issuecomment-1868010541

    Patched to be used with default traceback
    """

    if record["exception"] and RICH_ENABLED:
        output = io.StringIO()
        console = Console(file=output, force_terminal=True)
        trace = Traceback.from_exception(
            *record["exception"]
        )
        console.print(trace)
        record["extra"]["rich_exception"] = (
            output.getvalue()
        )
    if record["exception"] and not RICH_ENABLED:
        trace = record["exception"]

        record["extra"]["rich_exception"] = "\n".join(
            traceback.format_exception(*trace)
        )

    if record["exception"]:
        return FORMAT_ + "{extra[rich_exception]}"
    return FORMAT_


loggr.remove()
loggr.add(sys.stderr, format=rich_formatter)


class InterceptHandler(logging.Handler):
    """
    Source code: third block from https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        try:
            level: str | int = loggr.level(
                record.levelname
            ).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = (
                "importlib" in filename
                and "_bootstrap" in filename
            )
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1
        message = record.getMessage()

        loggr.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, message)


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[InterceptHandler()],
)
