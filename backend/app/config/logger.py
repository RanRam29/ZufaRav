# backend/app/config/logger.py

import logging

logger = logging.getLogger("zufarav")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(ch)
