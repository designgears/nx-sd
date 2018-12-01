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

    file_record_format = logging.Formatter(
        fmt='%(asctime)s - [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    Path('log').mkdir(parents=True, exist_ok=True)

    if logger.isEnabledFor(logging.ERROR):
        error_log_handler = logging.FileHandler('log/error.log')
        error_log_handler.setLevel(logging.ERROR)
        error_log_handler.setFormatter(file_record_format)
        logger.addHandler(error_log_handler)

    if logger.isEnabledFor(logging.DEBUG):
        debug_log_handler = logging.FileHandler('log/debug.log')
        debug_log_handler.setLevel(logging.DEBUG)
        debug_log_handler.setFormatter(file_record_format)
        logger.addHandler(debug_log_handler)


_setup_logging()
