"""Scam Shield: number-in-the-middle scam call interception.

Call flow
  1. Scammer dials TWILIO_NUMBER            -> POST /twilio/inbound
     TwiML: consent notice, then join conference "shield-<CallSid>".
     Server dials USER_PHONE (REST) with url=/twilio/user-leg.
  2. User leg answers                        -> POST /twilio/user-leg
     TwiML: <Start><Stream track="both_tracks"> to /media, then join conference.
     On the user's leg: inbound track = USER voice, outbound track = what the
     user hears = CALLER (conference mix). Two clean channels, no diarization.
  3. /media websocket                        -> two ScribeSessions -> Scorer
  4. Scorer alert                            -> announce warning to user leg,
                                                optionally remove caller.
"""
from __future__ import annotations

import asyncio
import base64
import json
import time
from pathlib import Path

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from . import config, intervene, prism
from .bus import bus
from .scorer import CallState, Scorer
from .transcriber import ScribeSession

from .browser_call import router as browser_router

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="Scam Shield")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
app.include_router(browser_router)

# conference name -> live call context
CALLS: dict[str, dict] = {}


# ---------------------------------------------------------------- dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard() -> str:
    return (ROOT / "static" / "dashboard.html").read_text()


@app.websocket("/dashboard")
async def dashboard_ws(ws: WebSocket):
    await bus.connect(ws)
    try:
        while True:
            msg = await ws.receive_text()
            data = json.loads(msg)
            if data.get("type") == "feedback":  # "Not a scam" button
                await prism.send_trace(data.get("trace_id", "unknown"), step="user_feedback",
                                       input="", output={"not_a_scam": True}, latency_ms=0, blocked=False)
                await bus.publish({"type": "feedback", "trace_id": data.get("trace_id")})
    except WebSocketDisconnect:
        bus.disconnect(ws)


# ---------------------------------------------------------------- twilio
def _twiml(body: str) -> Response:
    return Response(content=f'<?xml version="1.0" encoding="UTF-8"?><Response>{body}</Response>',
                    media_type="application/xml")


@app.post("/twilio/inbound")
async def twilio_inbound(request: Request):
    form = await request.form()
    caller_sid = form.get("CallSid", "")
    from_number = form.get("From", "")
    conf = f"shield-{caller_sid}"
    bus.reset()
    CALLS[conf] = {"caller_sid": caller_sid, "from": from_number, "started": time.time()}
    await bus.publish({"type": "status", "text": f"Inbound call from {from_number}. Bridging you in."})

    # dial the user in parallel; their leg carries the media stream
    try:
        user_sid = await asyncio.to_thread(intervene.dial_user, conf, caller_sid)
        CALLS[conf]["user_sid"] = user_sid
    except Exception as e:  # noqa: BLE001
        await bus.publish({"type": "status", "text": f"Failed to dial user: {e}"})

    return _twiml(
        '<Say voice="Polly.Joanna">This call may be monitored for fraud protection.</Say>'
        f'<Dial><Conference startConferenceOnEnter="true" endConferenceOnExit="true" '
        f'beep="false">{conf}</Conference></Dial>'
    )


@app.post("/twilio/user-leg")
async def twilio_user_leg(request: Request):
    conf = request.query_params.get("conf", "")
    caller = request.query_params.get("caller", "")
    ws_url = f"wss://{config.PUBLIC_HOST}/media?conf={conf}&caller={caller}"
    return _twiml(
        f'<Start><Stream url="{ws_url}" track="both_tracks"/></Start>'
        f'<Dial><Conference startConferenceOnEnter="true" endConferenceOnExit="true" '
        f'beep="false">{conf}</Conference></Dial>'
    )


@app.post("/twilio/warning")
@app.get("/twilio/warning")
async def twilio_warning():
    clip = ROOT / "static" / "warning.mp3"
    if clip.exists():
        return _twiml(f'<Play>https://{config.PUBLIC_HOST}/static/warning.mp3</Play>')
    return _twiml('<Say voice="Polly.Joanna">Warning. This call shows three signs of a scam. '
                  'Hang up now and call the number on the back of your card.</Say>')


# ---------------------------------------------------------------- media stream
@app.websocket("/media")
async def media_ws(ws: WebSocket):
    await ws.accept()
    conf = ws.query_params.get("conf", "")
    caller_sid = ws.query_params.get("caller", "")
    ctx = CALLS.setdefault(conf, {"caller_sid": caller_sid})
    state = CallState(trace_id=prism.new_trace_id(),
                      metadata={"direction": "inbound", "saved_contact": "no", "from": ctx.get("from", "")})
    ctx["state"] = state
    await bus.publish({"type": "status", "text": f"Stream connected. trace_id={state.trace_id}"})

    async def on_alert(result: dict) -> None:
        await bus.publish({"type": "alert", **result})
        user_sid = ctx.get("user_sid")
        if user_sid:
            ok = await intervene.warn_user(conf, user_sid)
            await bus.publish({"type": "status", "text": f"Warning played to user: {ok}"})
            if config.AUTO_KICK:
                asyncio.create_task(_kick(conf, ctx.get("caller_sid", "")))

    async def on_event(ev: dict) -> None:
        await bus.publish(ev)

    scorer = Scorer(on_alert=on_alert, on_event=on_event)

    async def on_transcript(speaker: str, text: str, committed: bool) -> None:
        if committed:
            await scorer.add_turn(state, speaker, text)
        else:
            await bus.publish({"type": "partial", "speaker": speaker, "text": text})

    # user leg: inbound = USER, outbound = CALLER (conference mix)
    sessions = {"inbound": ScribeSession("USER", on_transcript),
                "outbound": ScribeSession("CALLER", on_transcript)}
    for s in sessions.values():
        await s.start()

    try:
        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)
            ev = msg.get("event")
            if ev == "media":
                track = msg["media"].get("track", "inbound")
                payload = base64.b64decode(msg["media"]["payload"])
                sess = sessions.get(track)
                if sess:
                    sess.feed(payload)
            elif ev == "stop":
                break
    except WebSocketDisconnect:
        pass
    finally:
        for s in sessions.values():
            await s.stop()
        await bus.publish({"type": "status", "text": "Call ended."})


async def _kick(conf: str, caller_sid: str) -> None:
    ok = await intervene.kick_caller(conf, caller_sid, delay=config.KICK_CALLER_AFTER_SECONDS)
    await bus.publish({"type": "status", "text": f"Caller removed from call: {ok}"})


# ---------------------------------------------------------------- text harness
@app.post("/simulate")
async def simulate(request: Request):
    """POST {"lines": ["CALLER: ...", "USER: ..."]} to run the scorer without audio.
    Used by scripts/replay.py and as the stage fallback."""
    body = await request.json()
    bus.reset()
    state = CallState(trace_id=prism.new_trace_id(), metadata=body.get("metadata", {"direction": "inbound"}))
    results = []

    async def on_alert(result):  # no Twilio in simulate mode
        await bus.publish({"type": "alert", **result})

    scorer = Scorer(on_alert=on_alert, on_event=bus.publish)
    for line in body.get("lines", []):
        speaker, _, text = line.partition(":")
        r = await scorer.add_turn(state, speaker.strip().upper(), text)
        if r:
            results.append(r)
    return {"trace_id": state.trace_id, "alerted": state.alerted, "results": results}
