import logging
import os
import sys

_LOGGING_INITIALIZED = False


def get_logger(name: str) -> logging.Logger:
    global _LOGGING_INITIALIZED

    if not _LOGGING_INITIALIZED:
        _LOGGING_INITIALIZED = True

        debug = os.environ.get("PYTEST_UNASYNC_DEBUG", "")
        if debug.lower() in ("1", "true"):
            logger = logging.getLogger("pytest_unasync")
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stderr)
            logger.addHandler(handler)

    return logging.getLogger(name)
