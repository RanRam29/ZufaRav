from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 🔗 ראוטים רגילים
from routes.auth import router as auth_router
from routes.events import router as events_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router
from routes.admin_routes import router as admin_router
from routes.ws import ws_router

import logging

# ✅ הגדרות לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🎯 הגדרות CORS מדויקות
origins = [
    "https://zufa-rav.vercel.app",  # כתובת ה-Frontend
    "http://localhost:5173",        # local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # הרשה את כל השיטות
    allow_headers=["*"],      # הרשה את כל הכותרות
    expose_headers=["*"],     # חשוף כותרות גם לדפדפן
)

# 🔥 דיבוג ראשוני כשהשרת עולה
logger.info(f"✅ ZufaRav API Server started with allowed origins: {origins}")

# ✨ קריאת שורש לדיבוג חי
@app.get("/")
async def root():
    logger.info("📡 Root endpoint '/' called.")
    return JSONResponse(content={"status": "✅ ZufaRav backend is running"})

# ✅ כולל את כל ה־routers
app.include_router(auth_router)
logger.info("🔗 Auth routes loaded.")

app.include_router(events_router)
logger.info("🔗 Events routes loaded.")

app.include_router(reports_router)
logger.info("🔗 Reports routes loaded.")

app.include_router(tracking_router)
logger.info("🔗 Tracking routes loaded.")

app.include_router(admin_router)
logger.info("🔗 Admin routes loaded.")

app.include_router(ws_router)
logger.info("🔗 WebSocket routes loaded.")

# 🔥 טיפול כללי בשגיאות בשרת
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Unhandled server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred. The issue was logged."}
    )
