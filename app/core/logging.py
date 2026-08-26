import logging


def configure_logging() -> None:
    root_logger = logging.getLogger()

    root_logger.setLevel(logging.INFO)

    if not root_logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)