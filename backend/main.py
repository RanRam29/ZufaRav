from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ZufaRav.backend import auth
from routes import events, reports, tracking  # כולל tracking אם אתה משתמש בו


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או ["https://zufarav.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ראוט ברירת מחדל
@app.get("/")
async def root():
    return JSONResponse(content={"status": "✅ ZufaRav backend is running"})

# שאר הראוטים
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(reports.router)
app.include_router(tracking.router)  # אם tracking בשימוש
