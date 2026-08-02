"""
Real-time audio calling app — signaling server.

WebRTC handles the actual audio stream peer-to-peer (browser to browser),
so once a call connects, audio does NOT pass through this server — that's
what keeps latency minimal. This server's only job is "signaling": helping
two browsers in the same room exchange connection info (SDP offers/answers
and ICE candidates) so they can find each other and open a direct link.
"""

import json
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Real-Time Audio Call")

# room_id -> list of connected websockets (max 2 per room)
rooms: Dict[str, List[WebSocket]] = {}


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    room = rooms.setdefault(room_id, [])

    if len(room) >= 2:
        await websocket.send_text(json.dumps({"type": "room-full"}))
        await websocket.close()
        return

    room.append(websocket)
    is_initiator = len(room) == 1
    await websocket.send_text(json.dumps({"type": "joined", "initiator": is_initiator}))

    # Let the first peer know someone else has joined so it can start the offer
    if len(room) == 2:
        for peer in room:
            await peer.send_text(json.dumps({"type": "peer-joined"}))

    try:
        while True:
            data = await websocket.receive_text()
            # Relay signaling messages (offer / answer / ice-candidate) to the other peer
            for peer in room:
                if peer is not websocket:
                    await peer.send_text(data)
    except WebSocketDisconnect:
        if websocket in room:
            room.remove(websocket)
        for peer in room:
            try:
                await peer.send_text(json.dumps({"type": "peer-left"}))
            except Exception:
                pass
        if not room:
            rooms.pop(room_id, None)


# Static files (HTML/CSS/JS) mounted last so it doesn't shadow the routes above
app.mount("/static", StaticFiles(directory="static"), name="static")