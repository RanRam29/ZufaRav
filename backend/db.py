import sqlite3

# פונקציה שמחזירה חיבור חדש ל־tzukrav.db בכל קריאה
def get_db():
    return sqlite3.connect("tzukrav.db")
