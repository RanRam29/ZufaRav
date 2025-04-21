from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.auth import router as auth_router
from routes.events import router as events_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router
from routes.admin_routes import router as admin_router  # אופציונלי אם קיים

app = FastAPI()

# 🎯 הגדרות CORS - מונעות שגיאת Cross-Origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 אפשר לשים: ["https://zufarav.vercel.app"] בפרודקשן
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ בדיקת חיים
@app.get("/")
async def root():
    return JSONResponse(content={"status": "✅ ZufaRav backend is running"})

# 🔗 חיבור כל הראוטים
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(reports_router)
app.include_router(tracking_router)
app.include_router(admin_router)  # אופציונלי אם יש admin routes
