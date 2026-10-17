"""ElevenLabs Scribe v2 Realtime client, one session per audio track.

Twilio sends 8 kHz mu-law in 20 ms frames (160 bytes). We buffer ~250 ms,
convert to 16-bit PCM (or pass raw mu-law), base64 it, and send.

Protocol per ElevenLabs docs (server-side streaming guide):
  URL: wss://api.elevenlabs.io/v1/speech-to-text/realtime?model_id=scribe_v2_realtime
  Header: xi-api-key
  Client -> {"message_type":"input_audio_chunk","audio_base_64":"...","sample_rate":8000,"commit":false}
  Server -> {"message_type":"session_started"|"partial_transcript"|"committed_transcript"|..., "text": "..."}

VERIFY at the event: the query-param name for audio format (we send
`audio_format`) and whether `sample_rate` goes in the URL or each message.
Both are isolated in _url() and _chunk_msg() below.
"""
from __future__ import annotations

import asyncio
import base64
import json
from typing import Awaitable, Callable

import websockets

from . import config

TranscriptFn = Callable[[str, str, bool], Awaitable[None]]  # (speaker, text, committed)

_MULAW_TABLE = None


def _mulaw_to_pcm16(data: bytes) -> bytes:
    global _MULAW_TABLE
    if _MULAW_TABLE is None:
        table = []
        for u in range(256):
            u = ~u & 0xFF
            sign = u & 0x80
            exponent = (u >> 4) & 0x07
            mantissa = u & 0x0F
            sample = ((mantissa << 3) + 0x84) << exponent
            sample -= 0x84
            table.append(-sample if sign else sample)
        _MULAW_TABLE = table
    out = bytearray(len(data) * 2)
    for i, b in enumerate(data):
        s = _MULAW_TABLE[b]
        out[2 * i:2 * i + 2] = s.to_bytes(2, "little", signed=True)
    return bytes(out)


class ScribeSession:
    def __init__(self, speaker: str, on_transcript: TranscriptFn):
        self.speaker = speaker
        self.on_transcript = on_transcript
        self._q: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._task: asyncio.Task | None = None
        self._buf = bytearray()

    def _url(self) -> str:
        return ("wss://api.elevenlabs.io/v1/speech-to-text/realtime"
                f"?model_id=scribe_v2_realtime&audio_format={config.SCRIBE_AUDIO_FORMAT}")

    def _chunk_msg(self, audio: bytes) -> str:
        if config.SCRIBE_AUDIO_FORMAT.startswith("pcm"):
            audio = _mulaw_to_pcm16(audio)
        return json.dumps({
            "message_type": "input_audio_chunk",
            "audio_base_64": base64.b64encode(audio).decode(),
            "sample_rate": 8000,
            "commit": False,
        })

    async def start(self) -> None:
        self._task = asyncio.create_task(self._run())

    def feed(self, mulaw_frame: bytes) -> None:
        self._buf.extend(mulaw_frame)
        if len(self._buf) >= 2000:  # ~250 ms at 8 kHz mu-law
            self._q.put_nowait(bytes(self._buf))
            self._buf.clear()

    async def stop(self) -> None:
        if self._buf:
            self._q.put_nowait(bytes(self._buf))
            self._buf.clear()
        self._q.put_nowait(None)
        if self._task:
            try:
                await asyncio.wait_for(self._task, timeout=5)
            except asyncio.TimeoutError:
                self._task.cancel()

    async def _run(self) -> None:
        headers = {"xi-api-key": config.ELEVENLABS_API_KEY}
        async with websockets.connect(self._url(), additional_headers=headers, max_size=None) as ws:
            async def sender():
                while True:
                    chunk = await self._q.get()
                    if chunk is None:
                        try:
                            await ws.send(json.dumps({"message_type": "input_audio_chunk",
                                                      "audio_base_64": "", "sample_rate": 8000, "commit": True}))
                        except Exception:  # noqa: BLE001
                            pass
                        return
                    await ws.send(self._chunk_msg(chunk))

            async def receiver():
                async for raw in ws:
                    try:
                        msg = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    mt = msg.get("message_type", "")
                    text = (msg.get("text") or "").strip()
                    if mt == "partial_transcript" and text:
                        await self.on_transcript(self.speaker, text, False)
                    elif mt.startswith("committed_transcript") and text:
                        await self.on_transcript(self.speaker, text, True)
                    elif mt in ("input_error", "error"):
                        print(f"[scribe:{self.speaker}] error: {msg}")

            send_task = asyncio.create_task(sender())
            recv_task = asyncio.create_task(receiver())
            await send_task
            await asyncio.sleep(1.5)  # let final commits arrive
            recv_task.cancel()
