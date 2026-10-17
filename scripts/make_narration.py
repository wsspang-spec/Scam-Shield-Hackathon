"""Generate the demo narration with ElevenLabs TTS -> demo/narration/*.mp3

Run on the laptop (needs ELEVENLABS_API_KEY in .env):
    python scripts/make_narration.py
    git add demo && git commit -m "narration" && git push
"""
import os, sys
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "demo" / "narration"; OUT.mkdir(parents=True, exist_ok=True)
VOICE_ID = sys.argv[1] if len(sys.argv) > 1 else "onwK4e9ZLuTAKqWW03F9"  # Daniel, calm narrator

SEGMENTS = {
    "01_open": (
        "Imposter scams took three and a half billion dollars last year, and the customer eats almost all of it. "
        "That's about to change. The UK made banks reimburse in 2024, and New York is suing to do the same here. "
        "Every fraud control a bank has runs on its side of the call. Scam Shield runs on the customer's side."
    ),
    "02_marcus_intro": (
        "First, a scam call. The caller is an ElevenLabs agent playing a bank fraud department. Watch the panel on the right."
    ),
    "03_marcus_after": (
        "He said fraud department, verify, suspicious charge. A real bank says all of that. "
        "Then he said, read me the code. A real bank never does. "
        "The PRISM guardrail blocked it before the model ran, hung up on him, and told the customer why. "
        "There was never a chance to read the code."
    ),
    "04_dana_intro": (
        "Now the call that breaks other detectors: a real bank agent, following real procedure."
    ),
    "05_dana_after": (
        "She asked for a zip code and date of birth, exactly like a scammer would. Published detectors hang up on this call one time in four. "
        "Scam Shield didn't hang up, and it didn't let the customer answer either, because that's enough to pass phone verification. "
        "It asked her for a reference number. She gave one, with no pressure. "
        "It ended the call and texted the customer the number on the back of their card. Her reaction was the verdict."
    ),
    "06_prism": (
        "Every decision runs through PRISM by Block Convey. The guardrail runs in block mode, before the model. "
        "The run it stopped is traced under the same ID, with the model never called. "
        "And root cause across five runs shows every scam, whatever the story, converging on the same extraction step. "
        "That is why the guardrail sits in front of the model."
    ),
    "07_close": (
        "Red, it hangs up. Amber, it redirects to a secure line. Green, nothing. "
        "Nicrron for the model, ElevenLabs for the voices, PRISM for every decision. "
        "The customer never verifies anything on a call they didn't place."
    ),
}

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
for name, text in SEGMENTS.items():
    audio = client.text_to_speech.convert(voice_id=VOICE_ID, text=text, model_id="eleven_turbo_v2_5",
                                          output_format="mp3_44100_128")
    p = OUT / f"{name}.mp3"
    with p.open("wb") as f:
        for chunk in audio:
            f.write(chunk)
    print("wrote", p)
