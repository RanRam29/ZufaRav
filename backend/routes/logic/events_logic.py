# backend/routes/logic/events_logic.py

from fastapi import HTTPException
from datetime import datetime
from app.config.logger import logger

# יצירת אירוע

def create_event_logic(event, conn):
    logger.debug(f"🔧 יצירת אירוע חדש: {event.title}")
    try:
        # ולידציה מקדימה
        required_fields = {
            "title": event.title,
            "location": event.location,
            "reporter": event.reporter,
            "severity": event.severity,
            "datetime": event.datetime,
            "lat": event.lat,
            "lng": event.lng
        }

        for field, value in required_fields.items():
            if value in [None, ""]:
                logger.error(f"❌ שדה חובה חסר: {field}")
                raise HTTPException(status_code=400, detail=f"שדה חובה חסר: {field}")

        # תיאום בין people_required ל־people_count
        people_required = getattr(event, "people_required", getattr(event, "people_count", 1))

        created_at = datetime.utcnow().isoformat()

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (
                    title, location, reporter, severity,
                    people_required, datetime, created_at,
                    confirmed, lat, lng, people_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event.title,
                event.location,
                event.reporter,
                event.severity,
                people_required,
                event.datetime,
                created_at,
                False,
                event.lat,
                event.lng,
                0
            ))

        conn.commit()
        logger.info(f"✅ אירוע '{event.title}' נוצר בהצלחה")
        return {"msg": "אירוע נוצר בהצלחה"}

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ שגיאה כללית ביצירת אירוע '{event.title}': {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה ביצירת אירוע")

# טעינת אירועים

def list_events_logic(conn):
    logger.debug("🔧 טעינת רשימת אירועים")
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events ORDER BY created_at DESC")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            events = [dict(zip(columns, row)) for row in rows]
        logger.info(f"✅ נטענו {len(events)} אירועים מהרשימה")
        return events
    except Exception as e:
        logger.error(f"❌ שגיאה בטעינת רשימת אירועים: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בטעינת רשימת אירועים")
