"""Mid-call intervention via Twilio Conference REST API.

Participants in a conference are addressed by their CallSid, so we need:
  conference friendly name  -> look up Conference SID
  user_call_sid             -> announce the warning to the USER leg only
  caller_call_sid           -> remove the caller after a delay
"""
from __future__ import annotations

import asyncio

from twilio.rest import Client

from . import config

_client: Client | None = None


def client() -> Client:
    global _client
    if _client is None:
        _client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    return _client


def warning_url() -> str:
    return f"https://{config.PUBLIC_HOST}/twilio/warning"


def _conference_sid(friendly_name: str) -> str | None:
    confs = client().conferences.list(friendly_name=friendly_name, status="in-progress", limit=1)
    return confs[0].sid if confs else None


async def warn_user(conference_name: str, user_call_sid: str) -> bool:
    """Play the warning clip into the user's ear. Caller does not hear it."""
    def _do():
        sid = _conference_sid(conference_name)
        if not sid:
            return False
        client().conferences(sid).participants(user_call_sid).update(announce_url=warning_url())
        return True
    return await asyncio.to_thread(_do)


async def kick_caller(conference_name: str, caller_call_sid: str, delay: int = 0) -> bool:
    if delay:
        await asyncio.sleep(delay)

    def _do():
        sid = _conference_sid(conference_name)
        if not sid:
            return False
        client().conferences(sid).participants(caller_call_sid).delete()
        return True
    return await asyncio.to_thread(_do)


def dial_user(conference_name: str, caller_call_sid: str) -> str:
    """Bridge the user's real phone into the conference with a media stream
    attached to the user's leg (both tracks). Returns the user leg CallSid."""
    call = client().calls.create(
        to=config.USER_PHONE,
        from_=config.TWILIO_NUMBER,
        url=f"https://{config.PUBLIC_HOST}/twilio/user-leg?conf={conference_name}&caller={caller_call_sid}",
    )
    return call.sid
