import logging

from pathlib import Path


class _LoggingSingleLevelFilter(logging.Filter):

    def __init__(self, level):
        self._level = level

    def filter(self, record):
        return record.levelno == self._level


def _setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.addFilter(_LoggingSingleLevelFilter(logging.INFO))
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(console_handler)

    Path('log').mkdir(parents=True, exist_ok=True)

    file_log_handler = logging.FileHandler('log/build.log', delay=True)
    file_log_handler.setLevel(logging.DEBUG)
    file_log_handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s - [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(file_log_handler)


_setup_logging()
