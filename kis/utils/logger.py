import logging

FORMAT = (
    "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d %(message)s"
)


def configure_logger(
        name: str = "kis", log_level: int = logging.INFO
) -> logging.Logger:
    """configure logger"""
    # get logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        # formatter
        formatter = logging.Formatter(FORMAT)

        # stream handler 추가
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger
