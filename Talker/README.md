# EchoLine — Real-Time Audio Calling

A peer-to-peer audio calling web app. Two users open the page, enter the same
room code, and talk — with near-zero latency because audio streams **directly
between the two browsers** via WebRTC. The FastAPI server is only used briefly
at the start, to help the two browsers find each other (this is called
"signaling") — it never touches the actual audio.

## How it works

1. Both users load the page and enter/share the same **room code**.
2. Each browser opens a WebSocket connection to `main.py` at `/ws/{room_id}`.
3. The server pairs the two sockets in that room and relays three kinds of
   messages between them: SDP **offer**, SDP **answer**, and **ICE
   candidates** — this is standard WebRTC handshake info, not audio data.
4. Once the handshake completes, an `RTCPeerConnection` opens a direct
   media path between the browsers (over the LAN if they're on the same
   network, or via STUN-assisted NAT traversal otherwise) and audio flows
   peer-to-peer from then on.
5. If the server restarts or goes down mid-call, the call itself keeps
   running — only starting a *new* call requires the server.

## Run it

```bash
cd audiocall
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open `http://localhost:8000` in two browser tabs (or two devices on the
same network, using your machine's local IP instead of `localhost`), enter
the same room code in both, and click **Join / Start Call**.

## Notes / next steps

- **Same-network calls**: work great as-is — STUN is enough for local/LAN
  and most home/office NATs.
- **Different-network / strict NAT calls**: if a connection occasionally
  fails to establish, add a TURN server (e.g. Twilio's or a self-hosted
  `coturn`) to the `ICE_SERVERS` list in `static/app.js` as a relay fallback.
- **Rooms are in-memory**: restarting the server clears active rooms. For
  production, you'd want Redis or similar if you scale to multiple server
  instances.
- **Security**: no auth on rooms right now — anyone with the code can join.
  Fine for a demo/portfolio piece; add a room password or token if you take
  this further.
- Video and screen-share could be added later by extending `getUserMedia`
  and adding a `<video>` element — the signaling logic barely changes.

## Project structure

```
audiocall/
├── main.py              # FastAPI app + WebSocket signaling server
├── requirements.txt
└── static/
    ├── index.html        # Landing screen + call UI
    ├── style.css
    └── app.js             # WebRTC + signaling client logic
```
