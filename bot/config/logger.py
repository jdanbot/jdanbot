import coloredlogs

import logging

from .lib.filters import NoRunningJobFilter, ResendLogs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s",
                    level="INFO",
                    logger=logger)

logging.getLogger("schedule").addFilter(NoRunningJobFilter())