from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.auth import router as auth_router
from routes.events import router as events_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router
from routes.admin_routes import router as admin_router  # אופציונלי

app = FastAPI()

# 🎯 הגדרות CORS מדויקות - מאפשרות גישה רק מה-Frontend
origins = [
    "https://zufa-8oyxxslz4-ranram29s-projects.vercel.app",  # Frontend שלך ב־Vercel
    "http://localhost:5173",  # פיתוח מקומי
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
app.include_router(admin_router)  # אם יש קובץ admin_routes
