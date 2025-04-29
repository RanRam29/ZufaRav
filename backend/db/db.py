
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config.logger import logger

MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

def get_db():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            logger.debug("📅 מנסה להתחבר למסד הנתונים...")
            conn = psycopg2.connect(
                dsn=os.getenv("DATABASE_URL"),
                cursor_factory=RealDictCursor
            )
            logger.info("📊 התחברות למסד הנתונים הצליחה.")
            return conn

        except psycopg2.OperationalError as e:
            logger.critical("❌ חיבור למסד נכשל: %s", str(e))
            retries += 1
            if retries < MAX_RETRIES:
                logger.warning("🔁 ניסיון חיבור נוסף (%d/%d)...", retries, MAX_RETRIES)
                time.sleep(RETRY_DELAY)
            else:
                logger.critical("❌ כל ניסיונות החיבור נכשלו.")
                raise e

        except Exception as e:
            logger.critical("❌ שגיאה לא צפויה: %s", str(e))
            raise e
