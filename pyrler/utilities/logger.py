import logging
import sys

logger = logging.getLogger('log')


def setup_handlers(log_stdout=True, log_file=None, log_level=None):
    # print(log_level)
    if log_level == "INFO":
        logger.setLevel(logging.INFO)
    elif log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif log_level == "WARN" or log_level == "WARNING":
        logger.setLevel(logging.WARN)
    elif log_level == "CRIT" or log_level == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)

    if log_stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)

        logger.addHandler(stdout_handler)

    if log_file:
        file_handler = logging.FileHandler(filename=log_file, mode='a+')

        logger.addHandler(file_handler)
