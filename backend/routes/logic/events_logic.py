# backend/routes/logic/events_logic.py

from fastapi import HTTPException
from datetime import datetime

# יצירת אירוע

def create_event_logic(event, conn):
    print(f"🔧 DEBUG: יצירת אירוע {event.title}")
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
        print("✅ DEBUG: אירוע נוצר בהצלחה")
        return {"msg": "אירוע נוצר בהצלחה"}
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR: יצירת אירוע נכשלה: {e}")
        raise HTTPException(status_code=500, detail="שגיאה ביצירת אירוע")


# טעינת אירועים

def list_events_logic(conn):
    print("🔧 DEBUG: טעינת רשימת אירועים")
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events ORDER BY created_at DESC")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            events = [dict(zip(columns, row)) for row in rows]
        print(f"✅ DEBUG: נטענו {len(events)} אירועים")
        return events
    except Exception as e:
        print(f"❌ ERROR: שגיאה בטעינת אירועים: {e}")
        raise HTTPException(status_code=500, detail="שגיאה בטעינת רשימת אירועים")


# אישור אירוע

def confirm_event_logic(title, username, conn):
    print(f"🔧 DEBUG: אישור אירוע {title} על ידי {username}")
    try:
        confirmed_at = datetime.utcnow()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE events
                SET confirmed = TRUE, confirmed_by = %s, confirmed_at = %s
                WHERE title = %s
            """, (username, confirmed_at, title))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
        conn.commit()
        print("✅ DEBUG: אירוע אושר בהצלחה")
        return {"msg": f"האירוע '{title}' אושר על ידי {username}"}
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR: שגיאה באישור אירוע: {e}")
        raise HTTPException(status_code=500, detail="שגיאה באישור אירוע")


# הצטרפות לאירוע

def join_event_logic(event_id, username, conn):
    print(f"🔧 DEBUG: {username} מצטרף לאירוע {event_id}")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO event_participants (event_id, username)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (event_id, username))
        conn.commit()
        print("✅ DEBUG: הצטרפות בוצעה בהצלחה")
        return {"msg": f"{username} נוסף לאירוע {event_id}"}
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR: שגיאה בהצטרפות לאירוע: {e}")
        raise HTTPException(status_code=500, detail="שגיאה בהצטרפות לאירוע")


# עדכון כמות משתתפים

def update_people_count_logic(event_id, new_count, conn):
    print(f"🔧 DEBUG: עדכון כמות משתתפים באירוע {event_id} ל-{new_count}")
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE events SET people_count = %s WHERE id = %s
            """, (new_count, event_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="אירוע לא נמצא")
        conn.commit()
        print("✅ DEBUG: עדכון כמות משתתפים בוצע")
        return {"msg": f"עודכנו {new_count} משתתפים לאירוע {event_id}"}
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR: שגיאה בעדכון משתתפים: {e}")
        raise HTTPException(status_code=500, detail="שגיאה בעדכון כמות משתתפים")


# מחיקת אירוע והעברה לארכיון

def delete_event_logic(event_id, username, conn):
    print(f"🔧 DEBUG: מחיקת אירוע {event_id} על ידי {username}")
    deleted_at = datetime.utcnow()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            original = cursor.fetchone()
            if not original:
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
        print("✅ DEBUG: אירוע נמחק והועבר לארכיון")
        return {"msg": f"אירוע {event_id} נמחק והועבר לארכיון"}
    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR: שגיאה במחיקת אירוע: {e}")
        raise HTTPException(status_code=500, detail="שגיאה במחיקת האירוע")


# טעינת ארכיון

def get_archived_events_logic(conn):
    print("🔧 DEBUG: טעינת אירועים מארכיון")
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
        print(f"✅ DEBUG: נטענו {len(archived)} אירועים מארכיון")
        return archived
    except Exception as e:
        print(f"❌ ERROR: שגיאה בטעינת ארכיון: {e}")
        raise HTTPException(status_code=500, detail="שגיאה בטעינת הארכיון")
