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
            sslmode="prefer"  # ✅ שינוי חשוב: מאפשר גם חיבור ללא SSL בעת צורך
        )

        logger.info(f"📊 INFO: חיבור למסד הנתונים '{os.getenv('POSTGRES_DB')}' הצליח בשרת '{os.getenv('POSTGRES_HOST')}'.")
        return conn

    except psycopg2.OperationalError as e:
        logger.critical(f"❌ CRITICAL: בעיית חיבור למסד הנתונים: {e}")
        raise e

    except Exception as e:
        logger.critical(f"❌ CRITICAL: שגיאה כללית במסד הנתונים: {e}")
        raise e