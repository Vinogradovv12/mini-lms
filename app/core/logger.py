import logging

logger = logging.getLogger("security")

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    "security.log"
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
