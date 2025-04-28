# backend/tests/test_logger.py

import os
from app.config.logger import log

def run_logger_tests():
    print("\n🔍 בדיקת מערכת לוגים...\n")

    # ניקוי קבצים ישנים אם קיימים (רק לצורך בדיקה)
    if os.path.exists("logs/zufarav.log"):
        os.remove("logs/zufarav.log")
    if os.path.exists("logs/error.log"):
        os.remove("logs/error.log")

    # הפעלת קריאות לוג
    log("debug", "📘 [DEBUG] הודעת דיבאג לבדיקה")
    log("info", "📗 [INFO] הודעת מידע לבדיקה")
    log("warning", "📙 [WARNING] הודעת אזהרה לבדיקה")
    log("error", "📕 [ERROR] הודעת שגיאה לבדיקה")
    log("critical", "📕 [CRITICAL] הודעת קריטית לבדיקה")

    print("✅ נשלחו הודעות לוג. עכשיו בודקים אם קבצי לוג נוצרו...")

    if os.path.exists("logs/zufarav.log"):
        print("✅ נמצא קובץ logs/zufarav.log")
    else:
        print("❌ קובץ logs/zufarav.log לא נוצר")

    if os.path.exists("logs/error.log"):
        print("✅ נמצא קובץ logs/error.log")
    else:
        print("❌ קובץ logs/error.log לא נוצר")

    # בדיקת התוכן
    with open("logs/zufarav.log", "r", encoding="utf-8") as f:
        zufarav_content = f.read()
    with open("logs/error.log", "r", encoding="utf-8") as f:
        error_content = f.read()

    assert "[DEBUG]" in zufarav_content, "לא נמצאה הודעת DEBUG בקובץ הראשי"
    assert "[INFO]" in zufarav_content, "לא נמצאה הודעת INFO בקובץ הראשי"
    assert "[WARNING]" in zufarav_content, "לא נמצאה הודעת WARNING בקובץ הראשי"
    assert "[ERROR]" in zufarav_content, "לא נמצאה הודעת ERROR בקובץ הראשי"
    assert "[CRITICAL]" in zufarav_content, "לא נמצאה הודעת CRITICAL בקובץ הראשי"

    assert "[ERROR]" in error_content, "לא נמצאה הודעת ERROR בקובץ error.log"
    assert "[CRITICAL]" in error_content, "לא נמצאה הודעת CRITICAL בקובץ error.log"

    print("\n🎯 כל הבדיקות עברו בהצלחה! מערכת לוגים תקינה.\n")

if __name__ == "__main__":
    run_logger_tests()
