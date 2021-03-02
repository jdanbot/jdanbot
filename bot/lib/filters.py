import logging


class NoRunningJobFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith("Running job Every")

