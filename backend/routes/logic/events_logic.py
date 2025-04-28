# backend/routes/logic/events_logic.py

from fastapi import HTTPException
from datetime import datetime
from app.config.logger import log

# יצירת אירוע
def create_event_logic(event, conn):
    log("debug", f"🔧 יצירת אירוע חדש: {event.title}")
    try:
        created_at = datetime.utcnow().isoformat()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (
                    title, location, reporter, severity,
                    people_required, datetime, created_at,
                    confirmed, lat, lng, people_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event.title, event.location, event.reporter,
                event.severity, event.people_required, event.datetime,
                created_at,
                False, event.lat, event.lng, 0
            ))
        conn.commit()
        log("info", f"✅ אירוע '{event.title}' נוצר בהצלחה")
        return {"msg": "אירוע נוצר בהצלחה"}
    except Exception as e:
        conn.rollback()
        log("error", f"❌ שגיאה ביצירת אירוע '{event.title}': {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה ביצירת אירוע")


# טעינת אירועים
def list_events_logic(conn):
    log("debug", "🔧 טעינת רשימת אירועים")
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events ORDER BY created_at DESC")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            events = [dict(zip(columns, row)) for row in rows]
        log("info", f"✅ נטענו {len(events)} אירועים מהרשימה")
        return events
    except Exception as e:
        log("error", f"❌ שגיאה בטעינת רשימת אירועים: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בטעינת רשימת אירועים")


# אישור אירוע
def confirm_event_logic(title, username, conn):
    log("debug", f"🔧 התחלת אישור אירוע '{title}' על ידי {username}")
    try:
        confirmed_at = datetime.utcnow()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE events
                SET confirmed = TRUE, confirmed_by = %s, confirmed_at = %s
                WHERE title = %s
            """, (username, confirmed_at, title))
            if cursor.rowcount == 0:
                log("warning", f"⚠️ ניסיון לאשר אירוע שלא נמצא: {title}")
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
        conn.commit()
        log("info", f"✅ האירוע '{title}' אושר בהצלחה על ידי {username}")
        return {"msg": f"האירוע '{title}' אושר על ידי {username}"}
    except Exception as e:
        conn.rollback()
        log("error", f"❌ שגיאה באישור אירוע '{title}': {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה באישור אירוע")


# הצטרפות לאירוע
def join_event_logic(event_id, username, conn):
    log("debug", f"🔧 {username} מצטרף לאירוע ID {event_id}")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO event_participants (event_id, username)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (event_id, username))
        conn.commit()
        log("info", f"✅ {username} נוסף בהצלחה לאירוע {event_id}")
        return {"msg": f"{username} נוסף לאירוע {event_id}"}
    except Exception as e:
        conn.rollback()
        log("error", f"❌ שגיאה בהצטרפות {username} לאירוע {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בהצטרפות לאירוע")


# עדכון כמות משתתפים
def update_people_count_logic(event_id, new_count, conn):
    log("debug", f"🔧 עדכון כמות משתתפים באירוע {event_id} ל-{new_count}")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE events SET people_count = %s WHERE id = %s
            """, (new_count, event_id))
            if cursor.rowcount == 0:
                log("warning", f"⚠️ ניסיון לעדכן אירוע שלא נמצא: ID {event_id}")
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
        conn.commit()
        log("info", f"✅ עודכנו {new_count} משתתפים לאירוע {event_id}")
        return {"msg": f"עודכנו {new_count} משתתפים לאירוע {event_id}"}
    except Exception as e:
        conn.rollback()
        log("error", f"❌ שגיאה בעדכון משתתפים באירוע {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בעדכון כמות משתתפים")


# מחיקת אירוע והעברה לארכיון
def delete_event_logic(event_id, username, conn):
    log("debug", f"🔧 התחלת מחיקת אירוע ID {event_id} על ידי {username}")
    deleted_at = datetime.utcnow()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            original = cursor.fetchone()
            if not original:
                log("warning", f"⚠️ ניסיון למחוק אירוע שלא נמצא: ID {event_id}")
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
            columns = [desc[0] for desc in cursor.description]
            event = dict(zip(columns, original))

            cursor.execute("""
                INSERT INTO events_archive (
                    id, title, location, reporter, lat, lng, address, datetime,
                    confirmed, confirmed_by, confirmed_at, created_at, arrival_time,
                    deleted_by, deleted_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event["id"], event["title"], event["location"], event["reporter"],
                event["lat"], event["lng"], event.get("address"), event["datetime"],
                event["confirmed"], event.get("confirmed_by"), event.get("confirmed_at"),
                event["created_at"], event.get("arrival_time"),
                username, deleted_at
            ))

            cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        conn.commit()
        log("info", f"✅ אירוע {event_id} נמחק והועבר לארכיון בהצלחה על ידי {username}")
        return {"msg": f"אירוע {event_id} נמחק והועבר לארכיון"}
    except Exception as e:
        conn.rollback()
        log("error", f"❌ שגיאה במחיקת אירוע {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה במחיקת האירוע")


# טעינת ארכיון
def get_archived_events_logic(conn):
    log("debug", "🔧 טעינת אירועים מארכיון")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT title, location, reporter, datetime, confirmed_by,
                       confirmed_at, arrival_time, deleted_by, deleted_at
                FROM events_archive
                ORDER BY deleted_at DESC
            """)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            archived = [dict(zip(columns, row)) for row in rows]
        log("info", f"✅ נטענו {len(archived)} אירועים מהארכיון")
        return archived
    except Exception as e:
        log("error", f"❌ שגיאה בטעינת אירועים מהארכיון: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בטעינת הארכיון")
