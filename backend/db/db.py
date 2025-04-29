# backend/app/db/db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config.logger import logger

def get_db():
    try:
        logger.debug("📅 DEBUG: מנסה להתחבר למסד הנתונים...")
        
        conn = psycopg2.connect(
            dsn=os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )

        logger.info("📊 INFO: חיבור למסד הנתונים הצליח.")
        return conn

    except psycopg2.OperationalError as e:
        logger.critical(f"❌ CRITICAL: בעיית חיבור למסד הנתונים: {e}")
        raise e

    except Exception as e:
        logger.critical(f"❌ CRITICAL: שגיאה כללית במסד הנתונים: {e}")
        raise e
