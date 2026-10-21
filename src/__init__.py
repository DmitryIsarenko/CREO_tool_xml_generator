import logging
from pathlib import Path


def configure_logging() -> None:
    """Configure package logging once without clearing previous records."""
    logger = logging.getLogger(__name__)
    if logger.handlers:
        return

    log_directory = Path(__file__).resolve().parent / 'logs'
    log_directory.mkdir(parents=True, exist_ok=True)
    logfile_handler = logging.FileHandler(
        log_directory / 'log.log', mode='a', encoding='utf-8'
    )
    console_handler = logging.StreamHandler()
    date_format = '%Y-%m-%d %H:%M:%S'
    logfile_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)-8s --- %(message)s --- '
        '%(name)s:%(lineno)s',
        datefmt=date_format,
    ))
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)-8s --- %(message)-80s --- '
        '%(name)s:%(lineno)s',
        datefmt=date_format,
    ))
    logger.setLevel(logging.DEBUG)
    for handler in (console_handler, logfile_handler):
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    logger.info('Logger <<%s>> started.', __name__)
