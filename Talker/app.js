// ---------- Elements ----------
const landing = document.getElementById("landing");
const callScreen = document.getElementById("call");
const roomInput = document.getElementById("roomInput");
const generateBtn = document.getElementById("generateBtn");
const joinBtn = document.getElementById("joinBtn");
const landingError = document.getElementById("landingError");
const roomLabel = document.getElementById("roomLabel");
const statusText = document.getElementById("statusText");
const timerText = document.getElementById("timerText");
const muteBtn = document.getElementById("muteBtn");
const hangupBtn = document.getElementById("hangupBtn");
const remoteAudio = document.getElementById("remoteAudio");
const pulse = document.getElementById("pulse");

// ---------- State ----------
let ws = null;
let pc = null;
let localStream = null;
let isInitiator = false;
let muted = false;
let timerInterval = null;
let secondsElapsed = 0;

// STUN servers only — enough for two peers on the same network / most NATs.
// (For strict corporate/symmetric NATs you'd add a TURN server too.)
const ICE_SERVERS = {
  iceServers: [{ urls: ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"] }],
};

const words = ["blue", "coral", "amber", "swift", "cedar", "lunar", "ember", "quartz", "vivid", "north"];
function randomRoomCode() {
  const w = words[Math.floor(Math.random() * words.length)];
  const n = Math.floor(10 + Math.random() * 89);
  return `${w}-${n}`;
}

generateBtn.addEventListener("click", () => {
  roomInput.value = randomRoomCode();
});

joinBtn.addEventListener("click", () => {
  const room = roomInput.value.trim().toLowerCase().replace(/\s+/g, "-");
  if (!room) {
    landingError.textContent = "Enter or generate a room code first.";
    return;
  }
  landingError.textContent = "";
  startCall(room);
});

async function startCall(room) {
  try {
    localStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
  } catch (err) {
    landingError.textContent = "Microphone access is required to make a call.";
    return;
  }

  roomLabel.textContent = room;
  showScreen(callScreen);
  setStatus("Connecting…");

  const protocol = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(`${protocol}://${location.host}/ws/${encodeURIComponent(room)}`);

  ws.onopen = () => setStatus("Waiting for other person to join…");

  ws.onmessage = async (event) => {
    const msg = JSON.parse(event.data);

    switch (msg.type) {
      case "room-full":
        setStatus("Room is full (2 people already on this code).");
        cleanupAndReturn();
        break;

      case "joined":
        isInitiator = msg.initiator;
        break;

      case "peer-joined":
        setStatus("Peer connected — establishing audio…");
        setupPeerConnection();
        if (isInitiator) await makeOffer();
        break;

      case "offer":
        setupPeerConnection();
        await pc.setRemoteDescription(new RTCSessionDescription(msg.sdp));
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        ws.send(JSON.stringify({ type: "answer", sdp: answer }));
        break;

      case "answer":
        await pc.setRemoteDescription(new RTCSessionDescription(msg.sdp));
        break;

      case "ice-candidate":
        if (msg.candidate && pc) {
          try {
            await pc.addIceCandidate(new RTCIceCandidate(msg.candidate));
          } catch (e) {
            console.warn("ICE candidate error", e);
          }
        }
        break;

      case "peer-left":
        setStatus("The other person left the call.");
        stopTimer();
        if (pc) { pc.close(); pc = null; }
        break;
    }
  };

  ws.onerror = () => setStatus("Connection error. Check the server.");
  ws.onclose = () => {
    if (statusText.textContent.indexOf("left") === -1) {
      setStatus("Disconnected.");
    }
  };
}

function setupPeerConnection() {
  if (pc) return;
  pc = new RTCPeerConnection(ICE_SERVERS);

  localStream.getTracks().forEach((track) => pc.addTrack(track, localStream));

  pc.onicecandidate = (event) => {
    if (event.candidate && ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "ice-candidate", candidate: event.candidate }));
    }
  };

  pc.ontrack = (event) => {
    remoteAudio.srcObject = event.streams[0];
  };

  pc.onconnectionstatechange = () => {
    if (pc.connectionState === "connected") {
      setStatus("Call connected");
      pulse.style.animationDuration = "2s";
      startTimer();
    } else if (["disconnected", "failed", "closed"].includes(pc.connectionState)) {
      stopTimer();
      setStatus("Call ended");
    }
  };
}

async function makeOffer() {
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);
  ws.send(JSON.stringify({ type: "offer", sdp: offer }));
}

// ---------- Controls ----------
muteBtn.addEventListener("click", () => {
  if (!localStream) return;
  muted = !muted;
  localStream.getAudioTracks().forEach((t) => (t.enabled = !muted));
  muteBtn.classList.toggle("muted", muted);
  muteBtn.textContent = muted ? "🔇" : "🎤";
});

hangupBtn.addEventListener("click", () => {
  cleanupAndReturn();
});

function cleanupAndReturn() {
  stopTimer();
  if (ws) { ws.close(); ws = null; }
  if (pc) { pc.close(); pc = null; }
  if (localStream) { localStream.getTracks().forEach((t) => t.stop()); localStream = null; }
  secondsElapsed = 0;
  timerText.textContent = "00:00";
  muted = false;
  muteBtn.classList.remove("muted");
  muteBtn.textContent = "🎤";
  showScreen(landing);
}

// ---------- Helpers ----------
function showScreen(screen) {
  document.querySelectorAll(".screen").forEach((s) => s.classList.remove("active"));
  screen.classList.add("active");
}

function setStatus(text) {
  statusText.textContent = text;
}

function startTimer() {
  stopTimer();
  timerInterval = setInterval(() => {
    secondsElapsed++;
    const m = String(Math.floor(secondsElapsed / 60)).padStart(2, "0");
    const s = String(secondsElapsed % 60).padStart(2, "0");
    timerText.textContent = `${m}:${s}`;
  }, 1000);
}

function stopTimer() {
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = null;
}