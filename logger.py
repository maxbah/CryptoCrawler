import logging


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Setup logger function

    :param name: logger_name.
    :param log_file: logger_file.
    :param level: logger level, default=INFO.
    :return: logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # handler
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(logging.ERROR)

    # formatter
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    # add handler
    logger.addHandler(handler)

    return logger