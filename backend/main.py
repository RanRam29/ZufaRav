from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import auth, events, reports

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או ["http://localhost:5173"] אם רוצים לאפשר רק מהממשק
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ראוט בסיסי כדי ש-Render ידע שהשרת פעיל
@app.get("/")
async def root():
    return JSONResponse(content={"status": "ZufaRav backend is running ✅"})

# ראוטים אמיתיים של המערכת
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(reports.router)
