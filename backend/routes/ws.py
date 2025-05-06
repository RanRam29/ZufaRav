from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config.logger import logger

ws_router = APIRouter()
connected_clients = []

@ws_router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info(f"🔗 לקוח התחבר לוובסוקט (סה\"כ {len(connected_clients)} מחוברים)")

    try:
        while True:
            await websocket.receive_text()  # שומר את החיבור פתוח
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logger.warning(f"🔌 לקוח התנתק מוובסוקט (סה\"כ {len(connected_clients)} מחוברים)")

async def broadcast_new_event(event_data):
    try:
        lat = float(event_data.get("lat"))
        lng = float(event_data.get("lng"))
    except (TypeError, ValueError):
        logger.warning(f"🚫 שידור בוטל – קואורדינטות לא תקינות: {event_data}")
        return

    if not event_data.get("title") or event_data.get("title") == "title":
        logger.warning(f"🚫 שידור בוטל – כותרת חסרה או דמה: {event_data}")
        return

    logger.debug(f"📡 שידור אירוע חדש: {event_data.get('title')} → {lat}, {lng}")

    for client in connected_clients.copy():
        try:
            await client.send_json({"type": "new_event", "data": event_data})
        except Exception as e:
            logger.error(f"❌ שגיאה בשליחת הודעה ללקוח: {str(e)}")
            if client in connected_clients:
                connected_clients.remove(client)
                logger.warning("⚠️ לקוח הוסר מהרשימה בעקבות כשל")
