# backend/routes/reports.py

# backend/routes/reports.py

from fastapi import APIRouter, Depends, HTTPException
from db.db import get_db
from routes.auth_utils import require_roles
from app.config.logger import logger


router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def report_summary(user=Depends(require_roles(["admin", "hamal", "rav", "user"]))):
    logger.info("📊 בקשת סיכום אירועים")
    conn = get_db()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT severity, COUNT(*) as count
            FROM events
            GROUP BY severity
        """)
        severity_stats = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) FROM event_participants
        """)
        join_count = cursor.fetchone()[0]

        logger.info(f"✅ סיכום אירועים נשלף בהצלחה - {len(severity_stats)} רמות חומרה")

        return {
            "severity_summary": [
                {"severity": row[0], "count": row[1]}
                for row in severity_stats
            ],
            "total_confirmations": join_count
        }

    except Exception as e:
        logger.error(f"❌ שגיאה בשליפת סיכום אירועים: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בסיכום הדוח")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            logger.debug("🔌 חיבור למסד נתונים נסגר אחרי שליפת סיכום")
