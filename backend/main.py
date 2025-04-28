from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ✅ קונפיגורציות
from app.config.logger import logger
from app.config.cors_settings import origins
from app.config.exception_handler import general_exception_handler

# ✅ טעינת ראוטרים חכמה
from app.core.routers_loader import include_routers

app = FastAPI()

# 🎯 קונפיגורציית CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
logger.info(f"✅ CORS middleware loaded with origins: {origins}")

# ✨ Endpoint בסיסי לבדיקה
@app.get("/")
async def root():
    logger.debug("📡 DEBUG: Root endpoint '/' called.")
    return JSONResponse(content={"status": "✅ ZufaRav backend is running"})

# 🔗 טעינת ראוטרים
try:
    include_routers(app)
    logger.info("✅ All routers loaded successfully.")
except Exception as e:
    logger.error(f"❌ ERROR: Failed to load routers: {e}")
    raise

# 🔥 טיפול גלובלי בשגיאות
app.add_exception_handler(Exception, general_exception_handler)
