from dotenv import load_dotenv
import psycopg2
import os
from app.config.logger import logger

# טעינת משתני סביבה
load_dotenv(dotenv_path=".env")

def get_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT", 5432)
        )
        logger.debug("🔌 חיבור למסד נתונים נוצר בהצלחה")
        return conn
    except Exception as e:
        logger.critical(f"❌ שגיאה ביצירת חיבור למסד נתונים: {str(e)}")
        raise
