"""PRISM by Block Convey integration.

Two responsibilities, mapped to the Trust & Risk proofs:

1. guardrail_evaluate(trace_id, text)  -> called BEFORE every model call.
   Block mode. If PRISM says block, the scorer never calls the model and the
   intervention fires directly. That blocked run is the "run it stopped."

2. send_trace(trace_id, ...)            -> sends the run under the SAME trace_id
   so the Guardrails page can show whether the block was honoured.

The request/response shapes below are a best guess at PRISM's REST API.
Open docs -> Guardrails and docs -> Traces at the event and adjust the two
_payload functions. Everything else in the app only depends on the
GuardrailResult dataclass, so you only touch this file.

If PRISM_ENDPOINT is blank, every call is a no-op except local logging to
logs/traces.jsonl, so the app runs end to end without PRISM.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path

import httpx

from . import config

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "traces.jsonl"
LOG_PATH.parent.mkdir(exist_ok=True)


@dataclass
class GuardrailResult:
    blocked: bool
    reason: str = ""
    rule: str = ""
    raw: dict = field(default_factory=dict)


def new_trace_id() -> str:
    return f"call-{uuid.uuid4().hex[:12]}"


# ---------------------------------------------------------------------------
# Local fallback guardrail. Mirrors the "dispositive" rubric items so the demo
# still blocks when PRISM is unreachable. PRISM's own guardrail should be
# authored with the same intent (see README, "Guardrail definition").
# ---------------------------------------------------------------------------
_LOCAL_RULES = [
    ("otp_readback", re.compile(
        r"\b(read|tell|give|text|type)\b.{0,40}\b(code|one[- ]time|otp|pin|password|cvv|security number)\b", re.I)),
    ("secret_request", re.compile(
        r"\b(full|entire|whole|complete)\b.{0,20}\b(social|ssn|card number|account number)\b", re.I)),
    ("irreversible_rail", re.compile(
        r"\b(gift card|apple card|google play card|bitcoin|crypto|atm kiosk|qr code|wire|western union|moneygram|cash|gold|courier|safe account|pay yourself|send (the )?money to yourself)\b", re.I)),
    ("secrecy", re.compile(
        r"\b(do not|don't|dont|cannot|can't|cant|must not|mustn't|never) (tell|inform|call|contact|mention|discuss)\b.{0,40}\b(anyone|anybody|bank|family|police|wife|husband|son|daughter|parents)\b|gag order", re.I)),
    # USER side: about to disclose a card number or SSN out loud
    ("user_pii_disclosure", re.compile(
        r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b|\b(?:\d[ -]?){15,16}\b")),
]


def _local_guardrail(text: str) -> GuardrailResult:
    for rule, rx in _LOCAL_RULES:
        m = rx.search(text)
        if m:
            return GuardrailResult(blocked=True, rule=rule, reason=f"matched '{m.group(0)}'")
    return GuardrailResult(blocked=False)


# ---------------------------------------------------------------------------
# PRISM calls. Adjust payload shapes to the docs.
# ---------------------------------------------------------------------------
def _headers() -> dict:
    return {"Authorization": f"Bearer {config.PRISM_API_KEY}", "Content-Type": "application/json"}


def _guardrail_payload(trace_id: str, text: str) -> dict:
    return {
        "trace_id": trace_id,
        "project": config.PRISM_PROJECT,
        "mode": "block",
        "input": text,
    }


def _trace_payload(trace_id: str, **kw) -> dict:
    return {"trace_id": trace_id, "project": config.PRISM_PROJECT, "timestamp": time.time(), **kw}


def _log_local(record: dict) -> None:
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(record) + "\n")


async def guardrail_evaluate(trace_id: str, text: str) -> GuardrailResult:
    """Block-mode guardrail. Always consults the local rules too, so a block is
    never missed if PRISM is down; PRISM's decision wins when it responds."""
    local = _local_guardrail(text)
    if not config.PRISM_ENDPOINT:
        _log_local({"kind": "guardrail", "trace_id": trace_id, "source": "local", **asdict(local)})
        return local
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.post(
                f"{config.PRISM_ENDPOINT.rstrip('/')}/api/guardrails/evaluate",
                headers=_headers(), json=_guardrail_payload(trace_id, text))
            r.raise_for_status()
            data = r.json()
        # Adjust these keys to the real response. Common shapes: {"action":"block"},
        # {"blocked":true}, {"decision":"BLOCK","reason":"..."}.
        blocked = (
            data.get("blocked") is True
            or str(data.get("action", data.get("decision", ""))).lower() == "block"
        )
        res = GuardrailResult(blocked=blocked, reason=str(data.get("reason", "")),
                              rule=str(data.get("rule", data.get("guardrail", ""))), raw=data)
        _log_local({"kind": "guardrail", "trace_id": trace_id, "source": "prism", **asdict(res)})
        return res
    except Exception as e:  # noqa: BLE001
        _log_local({"kind": "guardrail", "trace_id": trace_id, "source": "local-fallback", "error": str(e), **asdict(local)})
        return local


async def send_trace(trace_id: str, *, step: str, input: str, output: dict | str,
                     latency_ms: float, blocked: bool, model: str = "", extra: dict | None = None) -> None:
    record = _trace_payload(trace_id, step=step, input=input, output=output,
                            latency_ms=round(latency_ms, 1), blocked=blocked, model=model,
                            **(extra or {}))
    _log_local({"kind": "trace", **record})
    if not config.PRISM_ENDPOINT:
        return
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            await client.post(f"{config.PRISM_ENDPOINT.rstrip('/')}/api/traces",
                              headers=_headers(), json=record)
    except Exception as e:  # noqa: BLE001
        _log_local({"kind": "trace_error", "trace_id": trace_id, "error": str(e)})
