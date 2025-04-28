# backend/app/core/routers_loader.py

from routes.auth import router as auth_router
from routes.events_routes import router as events_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router
from routes.admin_routes import router as admin_router
from routes.ws import ws_router
from app.config.logger import logger

def include_routers(app):
    logger("debug", "🚀 התחלת טעינת כל הראוטרים...")

    app.include_router(auth_router)
    logger("info", "🔗 ראוטר Auth נטען")

    app.include_router(events_router)
    logger("info", "🔗 ראוטר Events נטען")

    app.include_router(reports_router)
    logger("info", "🔗 ראוטר Reports נטען")

    app.include_router(tracking_router)
    logger("info", "🔗 ראוטר Tracking נטען")

    app.include_router(admin_router)
    logger("info", "🔗 ראוטר Admin נטען")

    app.include_router(ws_router)
    logger("info", "🔗 ראוטר WebSocket נטען")

    logger("debug", "✅ סיום טעינת כל הראוטרים")
