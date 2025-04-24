from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()
connected_clients = []

@ws_router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # שומר את החיבור פתוח
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_new_event(event_data):
    for client in connected_clients:
        try:
            await client.send_json({"type": "new_event", "data": event_data})
        except:
            if client in connected_clients:
                connected_clients.remove(client)
