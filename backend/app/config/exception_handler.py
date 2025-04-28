# backend/app/config/exception_handler.py

from fastapi.responses import JSONResponse
from app.config.logger import logger

async def general_exception_handler(request, exc):
    logger.error(f"❌ Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "שגיאת שרת כללית. הצוות קיבל התרעה ונבדוק בהקדם."}
    )
