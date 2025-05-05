from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config.logger import logger

# ייבוא הראוטים לפי שמות הקבצים בפועל
from routes.auth import router as auth_router
from routes.events_routes import router as events_router
from routes.admin_routes import router as admin_router
from routes.geocode_router import router as geocode_router
from routes.ws import router as websocket_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router

app = FastAPI()

# CORS
origins = [
    "https://zufa-rav.vercel.app",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.critical(f"❌ Validation Error: {exc.errors()} | Body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": (await request.body()).decode("utf-8")}
    )

# Routers
logger.debug("🚀 התחלת טעינת כל הראוטרים...")
app.include_router(auth_router)
logger.info("🔗 ראוטר Auth נטען")

app.include_router(events_router)
logger.info("🔗 ראוטר Events נטען")

app.include_router(reports_router)
logger.info("🔗 ראוטר Reports נטען")

app.include_router(tracking_router)
logger.info("🔗 ראוטר Tracking נטען")

app.include_router(admin_router)
logger.info("🔗 ראוטר Admin נטען")

app.include_router(websocket_router)
logger.info("🔗 ראוטר WebSocket נטען")

app.include_router(geocode_router, prefix="/api")
logger.info("🔗 ראוטר Geocode נטען עם prefix /api")

logger.debug("✅ סיום טעינת כל הראוטרים")
logger.info("✅ All routers loaded successfully.")

@app.get("/")
def root():
    logger.debug("📡 DEBUG: Root endpoint '/' called.")
    return {"message": "ZufaRav Backend is up and running!"}
