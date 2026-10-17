"""Browser call mode: ElevenLabs Conversational AI agent plays the caller, the
user talks from the laptop mic. No telephony.

The ElevenLabs browser SDK does not expose the agent's raw output audio, so in
this mode we take the SDK's transcript events (source: "user" | "ai") and feed
them straight into the same Scorer the Twilio path uses. Scribe is bypassed
here; in Twilio mode it transcribes both legs. Same guardrail, same model,
same PRISM traces, same dashboard.

Endpoints
  GET  /api/agent-session?agent_id=...  -> {conversation_token} (WebRTC) or
                                           {signed_url} (WebSocket), fetched
                                           server-side so the API key stays here.
  WS   /browser-call                    -> page sends {"type":"turn","speaker":"CALLER"|"USER","text":...}
                                           server replies {"type":"alert", ...} when the scorer fires.
"""
from __future__ import annotations

import json

import httpx
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from . import config, prism
from .bus import bus
from .scorer import CallState, Scorer

router = APIRouter()
EL = "https://api.elevenlabs.io/v1/convai/conversation"


@router.get("/api/agent-session")
async def agent_session(agent_id: str, mode: str = "webrtc"):
    headers = {"xi-api-key": config.ELEVENLABS_API_KEY}
    async with httpx.AsyncClient(timeout=10) as c:
        if mode == "webrtc":
            r = await c.get(f"{EL}/token", params={"agent_id": agent_id}, headers=headers)
            if r.status_code == 200 and r.json().get("token"):
                return {"conversation_token": r.json()["token"], "mode": "webrtc"}
        r = await c.get(f"{EL}/get-signed-url", params={"agent_id": agent_id}, headers=headers)
        if r.status_code == 200 and r.json().get("signed_url"):
            return {"signed_url": r.json()["signed_url"], "mode": "websocket"}
    # public agent fallback: the page can start with agentId alone
    return JSONResponse({"agent_id": agent_id, "mode": "public", "note": "token endpoints failed; agent must be public"},
                        status_code=200)


@router.websocket("/browser-call")
async def browser_call(ws: WebSocket):
    await ws.accept()
    bus.reset()
    state = CallState(trace_id=prism.new_trace_id(),
                      metadata={"direction": "inbound", "saved_contact": "no", "channel": "browser-demo"})
    await bus.publish({"type": "status", "text": f"Browser call started. trace_id={state.trace_id}"})

    async def on_alert(result: dict) -> None:
        await bus.publish({"type": "alert", **result})
        try:
            await ws.send_text(json.dumps({"type": "alert", **result}, default=str))
        except Exception:  # noqa: BLE001
            pass

    scorer = Scorer(on_alert=on_alert, on_event=bus.publish)
    await ws.send_text(json.dumps({"type": "ready", "trace_id": state.trace_id}))
    try:
        while True:
            msg = json.loads(await ws.receive_text())
            if msg.get("type") == "turn":
                await scorer.add_turn(state, msg.get("speaker", "CALLER"), msg.get("text", ""))
            elif msg.get("type") == "partial":
                await bus.publish({"type": "partial", "speaker": msg.get("speaker", "CALLER"), "text": msg.get("text", "")})
            elif msg.get("type") == "end":
                break
    except WebSocketDisconnect:
        pass
    finally:
        await bus.publish({"type": "status", "text": "Call ended."})
