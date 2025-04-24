from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 🔗 ראוטים רגילים
from routes.auth import router as auth_router
from routes.events import router as events_router
from routes.reports import router as reports_router
from routes.tracking import router as tracking_router
from routes.admin_routes import router as admin_router

# ✅ חדש: ראוטר ל־WebSocket
from routes.ws import ws_router

app = FastAPI()

# 🎯 הגדרות CORS מדויקות
origins = [
    "https://zufa-rav.vercel.app",  # ✅ חשוב ללא /
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return JSONResponse(content={"status": "✅ ZufaRav backend is running"})

# ✅ כולל את כל ה־routers
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(reports_router)
app.include_router(tracking_router)
app.include_router(admin_router)
app.include_router(ws_router)  # ✅ WebSocket endpoint
