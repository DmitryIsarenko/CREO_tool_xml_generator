import logging

format_string_logfile = "%(asctime)s %(levelname)-8s --- %(message)s --- %(name)s:%(lineno)s"
format_string_console = "%(asctime)s %(levelname)-8s --- %(message)-80s --- %(name)s:%(lineno)s"
date_format = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
# logfile_handler = logging.FileHandler(filename="../logs/log.log", mode="w")
logfile_handler = logging.FileHandler(filename="./src/logs/log.log", mode="w")

console_formatter = logging.Formatter(fmt=format_string_console, datefmt=date_format)
logfile_formatter = logging.Formatter(fmt=format_string_logfile, datefmt=date_format)

console_handler.setFormatter(console_formatter)
logfile_handler.setFormatter(logfile_formatter)

console_handler.setLevel(level=logging.DEBUG)
logfile_handler.setLevel(level=logging.DEBUG)

logger.addHandler(console_handler)
logger.addHandler(logfile_handler)

logger.info(f"Logger <<{__name__}>> started.")