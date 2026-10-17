import os
from dotenv import load_dotenv

load_dotenv()


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes")


PUBLIC_HOST = os.getenv("PUBLIC_HOST", "localhost:8000")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER", "")
USER_PHONE = os.getenv("USER_PHONE", "")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
SCRIBE_AUDIO_FORMAT = os.getenv("SCRIBE_AUDIO_FORMAT", "pcm_8000")

NICRRON_BASE_URL = os.getenv("NICRRON_BASE_URL", "https://api.nicrron.ai/v1")
NICRRON_API_KEY = os.getenv("NICRRON_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "nicrron/fastest")

PRISM_ENDPOINT = os.getenv("PRISM_ENDPOINT", "")
PRISM_API_KEY = os.getenv("PRISM_API_KEY", "")
PRISM_PROJECT = os.getenv("PRISM_PROJECT", "scam-shield")

FRAUD_THRESHOLD = int(os.getenv("FRAUD_THRESHOLD", "55"))
UNCERTAIN_THRESHOLD = int(os.getenv("UNCERTAIN_THRESHOLD", "20"))
WINDOW_TURNS = int(os.getenv("WINDOW_TURNS", "8"))
HYSTERESIS_WINDOWS = int(os.getenv("HYSTERESIS_WINDOWS", "2"))
KICK_CALLER_AFTER_SECONDS = int(os.getenv("KICK_CALLER_AFTER_SECONDS", "5"))
AUTO_KICK = _bool("AUTO_KICK", True)
