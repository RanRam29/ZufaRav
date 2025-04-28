import os
import psycopg2
from app.config.logger import logger

def get_db():
    try:
        # קבלת פרטי התחברות מהסביבה
        db_params = {
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT", 5432),
            "sslmode": "require"  # חובה ב-Render לחיבור מאובטח
        }

        # יצירת חיבור למסד הנתונים
        conn = psycopg2.connect(**db_params)
        logger.debug(f"🔌 חיבור למסד נתונים נוצר בהצלחה: {db_params['host']}/{db_params['dbname']}")
        return conn

    except Exception as e:
        logger.critical(f"❌ שגיאה ביצירת חיבור למסד נתונים: {str(e)}")
        raise
