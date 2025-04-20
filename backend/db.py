import sqlite3
import os

def get_db():
    db_path = "tzukrav.db"
    if not os.path.exists(db_path):
        # צור קובץ DB ריק אם לא קיים (ימנע קריסה)
        open(db_path, 'w').close()
    return sqlite3.connect(db_path)
