from db import get_db
import os

print("Password loaded from env:", os.getenv("POSTGRES_PASSWORD"))  # בדיקה
conn = get_db()
print("✅ התחברת ל־PostgreSQL בהצלחה!")
conn.close()
