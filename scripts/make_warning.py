"""Generate the in-ear warning clip with ElevenLabs TTS -> static/warning.mp3.
Twilio <Play> serves it from /static/warning.mp3. Without this file the app
falls back to Twilio's built-in <Say> voice, which also works."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
TEXT = ("Warning. This call shows three signs of a scam. "
        "Hang up now and call the number on the back of your card. "
        "Never read a security code to anyone who called you.")
VOICE_ID = sys.argv[1] if len(sys.argv) > 1 else "21m00Tcm4TlvDq8ikWAM"  # Rachel

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
audio = client.text_to_speech.convert(voice_id=VOICE_ID, text=TEXT,
                                      model_id="eleven_turbo_v2_5", output_format="mp3_44100_128")
out = ROOT / "static" / "warning.mp3"
with out.open("wb") as f:
    for chunk in audio:
        f.write(chunk)
print(f"wrote {out}")
