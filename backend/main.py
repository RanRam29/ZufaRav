
from fastapi import FastAPI
from routes import auth, events, reports
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או ["http://localhost:5173"] אם רוצים לאפשר רק מהממשק
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(reports.router)
