
from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def summary():
    conn = sqlite3.connect("tzukrav.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(confirmed) FROM events")
    total, confirmed = cursor.fetchone()
    conn.close()
    return {
        "total_events": total or 0,
        "confirmed": confirmed or 0
    }
