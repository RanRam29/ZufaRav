# backend/routes/logger_test.py

from app.config.logger import logger

def test_logger():
    logger.debug("🔧 [TEST] This is a DEBUG log from logger_test.py.")
    logger.info("✅ [TEST] This is an INFO log from logger_test.py.")
    logger.warning("⚠️ [TEST] This is a WARNING log from logger_test.py.")
    logger.error("❌ [TEST] This is an ERROR log from logger_test.py.")
    logger.critical("🚨 [TEST] This is a CRITICAL log from logger_test.py.")

if __name__ == "__main__":
    test_logger()
