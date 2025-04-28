# backend/app/db/db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config.logger import logger

def get_db():
    try:
        logger.debug("📅 DEBUG: מנסה להתחבר למסד הנתונים...")
        
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT", 5432),
            sslmode=os.getenv("DB_SSLMODE", "require")  # אם לא הוגדר – ברירת מחדל 'require'
        )

        logger.info(f"📊 INFO: חיבור למסד הנתונים '{os.getenv('POSTGRES_DB')}' הצליח בשרת '{os.getenv('POSTGRES_HOST')}'.")
        return conn

    except Exception as e:
        logger.critical(f"❌ CRITICAL: שגיאה ביצירת חיבור למסד נתונים: {e}")
        raise e
