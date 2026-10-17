"""Generate the shield's challenge line with ElevenLabs TTS -> static/challenge.mp3.
This is what the audience hears when the shield speaks to the caller on the
customer's behalf. The same text is sent to the agent via sendUserMessage."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
TEXT = ("Hi, this is William's call screening assistant. He doesn't share personal "
        "details or codes on calls he didn't place. If you can give me a reference "
        "number, he'll call you back on the number printed on his card.")
VOICE_ID = sys.argv[1] if len(sys.argv) > 1 else "21m00Tcm4TlvDq8ikWAM"  # Rachel

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
audio = client.text_to_speech.convert(voice_id=VOICE_ID, text=TEXT,
                                      model_id="eleven_turbo_v2_5", output_format="mp3_44100_128")
out = ROOT / "static" / "challenge.mp3"
with out.open("wb") as f:
    for chunk in audio:
        f.write(chunk)
print(f"wrote {out}")
