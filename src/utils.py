from os import getenv
import sys
from loguru import logger


LOGGER_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)


def enable_logger():
    return getenv("LOGGER_ENABLE", "1") == "1"


def init_logger(
    log_level: str, log_path: str | None = None, enable_logger: bool = True
) -> None:
    logger.remove()

    if enable_logger:
        logger.add(
            sys.stderr, colorize=True, format=LOGGER_FORMAT, level=log_level
        )
        if log_path:
            logger.add(
                log_path,
                level=log_level,
                format=LOGGER_FORMAT,
                rotation="16 MB",
                compression="zip",
                serialize=True,
            )
