# backend/routes/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config.logger import log

ws_router = APIRouter()
connected_clients = []

@ws_router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    log("info", f"🔗 לקוח התחבר לוובסוקט (סה״כ {len(connected_clients)} מחוברים)")

    try:
        while True:
            await websocket.receive_text()  # שומר את החיבור פתוח
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        log("warning", f"🔌 לקוח התנתק מוובסוקט (סה״כ {len(connected_clients)} מחוברים)")

async def broadcast_new_event(event_data):
    log("debug", f"📡 שידור אירוע חדש לכל הלקוחות: {event_data.get('title', 'ללא כותרת')}")
    for client in connected_clients:
        try:
            await client.send_json({"type": "new_event", "data": event_data})
        except Exception as e:
            log("error", f"❌ שגיאה בשליחת הודעה ללקוח: {str(e)}")
            if client in connected_clients:
                connected_clients.remove(client)
                log("warning", "⚠️ הוסר לקוח עם בעיה מהחיבורים הפעילים")
