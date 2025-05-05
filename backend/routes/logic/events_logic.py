from fastapi import HTTPException
from datetime import datetime
from app.config.logger import logger

def create_event_logic(event, conn):
    logger.debug(f"🔧 יצירת אירוע חדש: {getattr(event, 'title', '---')}")
    try:
        logger.debug(f"📥 נתוני האירוע המתקבלים: {event.__dict__ if hasattr(event, '__dict__') else event}")

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
                logger.error(f"❌ שדה חובה חסר: {field} (ערך: {value})")
                raise HTTPException(status_code=400, detail=f"שדה חובה חסר: {field}")

        people_required = getattr(event, "people_required", 1)
        people_count = getattr(event, "people_count", 0)  # 👈 זה החלק שהשתנה
        address = getattr(event, "address", "")
        created_at = datetime.utcnow().isoformat()

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (
                    title, location, reporter, severity,
                    people_required, datetime, created_at,
                    confirmed, lat, lng, address, people_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                address,
                people_count  # 👈 הכנסנו את הערך הנכון מה-Frontend
            ))

        conn.commit()
        logger.info(f"✅ אירוע '{event.title}' נוצר בהצלחה")
        return {"msg": "אירוע נוצר בהצלחה"}

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        logger.exception(f"❌ שגיאה כללית ביצירת אירוע '{getattr(event, 'title', '---')}': {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה ביצירת אירוע")


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
        logger.exception(f"❌ שגיאה בטעינת רשימת אירועים: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בטעינת רשימת אירועים")

def confirm_event_logic(title, username, conn):
    logger.debug(f"🔧 התחלת אישור אירוע '{title}' על ידי {username}")
    try:
        confirmed_at = datetime.utcnow()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE events
                SET confirmed = TRUE, confirmed_by = %s, confirmed_at = %s
                WHERE title = %s
            """, (username, confirmed_at, title))
            if cursor.rowcount == 0:
                logger.warning(f"⚠️ ניסיון לאשר אירוע שלא נמצא: {title}")
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
        conn.commit()
        logger.info(f"✅ האירוע '{title}' אושר בהצלחה על ידי {username}")
        return {"msg": f"האירוע '{title}' אושר על ידי {username}"}
    except Exception as e:
        conn.rollback()
        logger.exception(f"❌ שגיאה באישור אירוע '{title}': {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה באישור אירוע")

def join_event_logic(event_id, username, conn):
    logger.debug(f"🔧 {username} מצטרף לאירוע ID {event_id}")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO event_participants (event_id, username)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (event_id, username))
        conn.commit()
        logger.info(f"✅ {username} נוסף בהצלחה לאירוע {event_id}")
        return {"msg": f"{username} נוסף לאירוע {event_id}"}
    except Exception as e:
        conn.rollback()
        logger.exception(f"❌ שגיאה בהצטרפות {username} לאירוע {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בהצטרפות לאירוע")

def update_people_count_logic(event_id, new_count, conn):
    logger.debug(f"🔧 עדכון כמות משתתפים לאירוע ID {event_id} ל-{new_count}")
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            event = cursor.fetchone()
            if not event:
                logger.warning(f"⚠️ אירוע לא נמצא: ID {event_id}")
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")

            cursor.execute("""
                UPDATE events
                SET people_count = %s
                WHERE id = %s
            """, (new_count, event_id))

        conn.commit()
        logger.info(f"✅ עודכנה כמות משתתפים באירוע ID {event_id} ל-{new_count}")
        return {"msg": f"כמות המשתתפים עודכנה ל-{new_count} עבור האירוע ID {event_id}"}

    except Exception as e:
        conn.rollback()
        logger.exception(f"❌ שגיאה בעדכון כמות משתתפים לאירוע {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בעדכון כמות משתתפים")

def delete_event_logic(event_id, username, conn):
    logger.debug(f"🔧 התחלת מחיקת אירוע ID {event_id} על ידי {username}")
    deleted_at = datetime.utcnow()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            original = cursor.fetchone()
            if not original:
                logger.warning(f"⚠️ ניסיון למחוק אירוע שלא נמצא: ID {event_id}")
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
        logger.info(f"✅ אירוע {event_id} נמחק והועבר לארכיון בהצלחה על ידי {username}")
        return {"msg": f"אירוע {event_id} נמחק והועבר לארכיון"}
    except Exception as e:
        conn.rollback()
        logger.exception(f"❌ שגיאה במחיקת אירוע {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה במחיקת האירוע")

def get_archived_events_logic(conn):
    logger.debug("🔧 טעינת אירועים מארכיון")
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
        logger.info(f"✅ נטענו {len(archived)} אירועים מהארכיון")
        return archived
    except Exception as e:
        logger.exception(f"❌ שגיאה בטעינת אירועים מהארכיון: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה בטעינת הארכיון")
