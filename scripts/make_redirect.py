"""Generate the shield's redirect line with ElevenLabs TTS -> static/redirect.mp3."""
import os, sys
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
TEXT = ("This is William's call screening. He doesn't share personal details on calls he didn't place. "
        "Please provide a reference number and he'll call you back on the number on his card.")
VOICE_ID = sys.argv[1] if len(sys.argv) > 1 else "21m00Tcm4TlvDq8ikWAM"
client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
audio = client.text_to_speech.convert(voice_id=VOICE_ID, text=TEXT, model_id="eleven_turbo_v2_5", output_format="mp3_44100_128")
out = ROOT / "static" / "redirect.mp3"
with out.open("wb") as f:
    for chunk in audio:
        f.write(chunk)
print(f"wrote {out}")
