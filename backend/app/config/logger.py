# backend/app/config/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("zufarav")
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Console handler (לדפדפן או למסך)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# File handler - All logs (info+debug+warning+error+critical)
file_handler_all = RotatingFileHandler(
    "logs/zufarav.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
file_handler_all.setLevel(logging.DEBUG)
file_handler_all.setFormatter(formatter)

# File handler - Only errors
file_handler_errors = RotatingFileHandler(
    "logs/error.log",
    maxBytes=2 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler_errors.setLevel(logging.ERROR)
file_handler_errors.setFormatter(formatter)

# הוספת Handlers פעם אחת בלבד
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler_all)
    logger.addHandler(file_handler_errors)

# פונקציה חכמה לשימוש פשוט בלוגים
def log(level: str, message: str):
    """פונקציה חכמה ללוגים לפי רמת חומרה."""
    level = level.lower()
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)
    else:
        logger.info(message)  # ברירת מחדל אם לא נבחרה רמה נכונה
