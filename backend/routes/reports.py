from fastapi import APIRouter, Depends
from db import get_db
from auth_utils import require_roles

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def report_summary(user=Depends(require_roles(["admin", "hamal", "rav", "user"]))):
    conn = get_db()
    cursor = conn.cursor()

    # דוגמת סיכום: כמה אירועים יש לפי דרגת חומרה
    cursor.execute("""
        SELECT severity, COUNT(*) as count
        FROM events
        GROUP BY severity
    """)
    severity_stats = cursor.fetchall()

    # כמה אישורים ניתנו
    cursor.execute("""
        SELECT COUNT(*) FROM event_participants
    """)
    join_count = cursor.fetchone()[0]

    conn.close()

    return {
        "severity_summary": [
            {"severity": row[0], "count": row[1]}
            for row in severity_stats
        ],
        "total_confirmations": join_count
    }
