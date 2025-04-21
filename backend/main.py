from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.auth import router as auth_router
from routes.events import router as events_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router

app = FastAPI()

# הגדרות CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # אפשר לשים את ה-URL של הפרונטנד בלבד
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# בדיקת חיים
@app.get("/")
async def root():
    return JSONResponse(content={"status": "✅ ZufaRav backend is running"})

# רישום כל הראוטרים
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(reports_router)
app.include_router(tracking_router)
