import logging

from app.core.logging import configure_logging, get_logger


def test_get_logger_returns_logger():
    logger = get_logger("test")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"


def test_configure_logging_sets_info_level():
    configure_logging()

    logger = get_logger("test")

    assert logger.isEnabledFor(logging.INFO)