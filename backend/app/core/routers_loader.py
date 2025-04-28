# backend/app/core/routers_loader.py

from routes.auth import router as auth_router
from routes.events_routes import router as events_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router
from routes.admin_routes import router as admin_router
from routes.ws import ws_router
from config.logger import logger

def include_routers(app):
    logger.debug("🔧 DEBUG: מתחיל טעינת ראוטרים...")

    app.include_router(auth_router)
    logger.info("🔗 Auth routes loaded.")
    logger.debug("✅ DEBUG: auth_router loaded.")

    app.include_router(events_router)
    logger.info("🔗 Events routes loaded.")
    logger.debug("✅ DEBUG: events_router loaded.")

    app.include_router(reports_router)
    logger.info("🔗 Reports routes loaded.")
    logger.debug("✅ DEBUG: reports_router loaded.")

    app.include_router(tracking_router)
    logger.info("🔗 Tracking routes loaded.")
    logger.debug("✅ DEBUG: tracking_router loaded.")

    app.include_router(admin_router)
    logger.info("🔗 Admin routes loaded.")
    logger.debug("✅ DEBUG: admin_router loaded.")

    app.include_router(ws_router)
    logger.info("🔗 WebSocket routes loaded.")
    logger.debug("✅ DEBUG: ws_router loaded.")

    logger.debug("🏁 DEBUG: סיום טעינת כל הראוטרים.")
