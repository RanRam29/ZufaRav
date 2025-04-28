# backend/app/config/logger.py

import logging
import os
import requests
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# טעינת משתנים מה-.env
load_dotenv()

BETTERSTACK_TOKEN = os.getenv("BETTERSTACK_TOKEN")
BETTERSTACK_SOURCE = os.getenv("BETTERSTACK_SOURCE")
BETTERSTACK_HOST = os.getenv("BETTERSTACK_HOST")

# יצירת תיקיית לוגים לוקאלית (אם לא קיימת)
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("zufarav")
logger.setLevel(logging.DEBUG)

# פורמט בסיסי
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 📋 Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# 📋 File Handler (לשמירה מקומית)
file_handler = RotatingFileHandler(
    "logs/zufarav.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# 📡 BetterStack Cloud Handler
class BetterStackHandler(logging.Handler):
    def emit(self, record):
        if not (BETTERSTACK_TOKEN and BETTERSTACK_SOURCE and BETTERSTACK_HOST):
            return  # אם אין משתנים מהסביבה, לא לשלוח
        log_entry = self.format(record)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BETTERSTACK_TOKEN}",
        }
        payload = {
            "source": BETTERSTACK_SOURCE,
            "message": log_entry
        }
        try:
            requests.post(
                f"https://{BETTERSTACK_HOST}/",
                json=payload,
                headers=headers,
                timeout=5
            )
        except Exception as e:
            print(f"❌ Failed to send log to BetterStack: {e}")

# יצירת Cloud Handler
cloud_handler = BetterStackHandler()
cloud_handler.setLevel(logging.INFO)
cloud_handler.setFormatter(formatter)

# 🎯 חיבור כל ה-Handlers ללוגר
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(cloud_handler)

# פונקציה חכמה ללוגים
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
        logger.info(message)  # ברירת מחדל
