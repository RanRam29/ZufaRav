# backend/routes/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config.logger import logger

router = APIRouter()  # ✅ שונה מ־ws_router

connected_clients = []

@router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info(f"🔗 לקוח התחבר לוובסוקט (סה\"כ {len(connected_clients)} מחוברים)")

    try:
        while True:
            await websocket.receive_text()  # שמירה על חיבור פתוח
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logger.warning(f"🔌 לקוח התנתק מוובסוקט (סה\"כ {len(connected_clients)} מחוברים)")

async def broadcast_new_event(event_data):
    logger.debug(f"📡 שידור אירוע חדש: {event_data.get('title', 'ללא כותרת')}")
    for client in connected_clients:
        try:
            await client.send_json({"type": "new_event", "data": event_data})
        except Exception as e:
            logger.error(f"❌ שגיאה בשליחה ללקוח: {str(e)}")
            if client in connected_clients:
                connected_clients.remove(client)
                logger.warning("⚠️ לקוח הוסר מהרשימה")
