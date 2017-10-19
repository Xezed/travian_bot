import logging
import sys

from utils import add_seconds_to_datetime_now


def get_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%H:%M:%S')

    # Logging to file and on the screen.
    handler = logging.FileHandler('log.txt', mode='w')
    screen_handler = logging.StreamHandler(stream=sys.stdout)

    handler.setFormatter(formatter)
    screen_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(screen_handler)

    return logger


future_logger = get_logger('future_logger')


def info_logger_for_future_events(message, seconds):
    """Add assigned amount of seconds to the current timestamp and add new timestamp to the end of message."""

    timestamp = add_seconds_to_datetime_now(seconds)
    future_logger.info(message + str(timestamp))
