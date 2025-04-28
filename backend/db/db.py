import psycopg2
import os
from app.config.logger import logger

def get_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT", 5432),
            sslmode="require"  # חשוב מאוד ב-Render כדי להתחבר עם SSL
        )
        logger.debug("🔌 חיבור למסד נתונים נוצר בהצלחה")
        return conn
    except Exception as e:
        logger.critical(f"❌ שגיאה ביצירת חיבור למסד נתונים: {str(e)}")
        raise
