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
    # v1 only matched verb-before-noun ("read me the code"). A live run of the Marcus agent
    # said "sending a security code ... please read it back to me" and slipped to the model.
    # v2 matches either order within the same window.
    # v3: "confirm the billing zip code" (a legitimate identity check) matched on "code".
    # Exclude zip/area/postal/country code.
    ("otp_readback", re.compile(
        r"\b(read|tell|give|text|type|repeat|confirm)\b.{0,40}\b(?<!zip )(?<!area )(?<!postal )(?<!country )(code|one[- ]time|otp|pin|password|cvv|security number)\b"
        r"|\b(?<!zip )(?<!area )(?<!postal )(?<!country )(code|one[- ]time|otp|pin|password|cvv)\b.{0,80}\b(read|tell|give|text|type|repeat)\b.{0,20}\b(it|that|them|me)\b", re.I)),
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
# PRISM calls, matched to docs -> Guardrails and docs -> Traces.
#
# Auth is the API-key header, not "Authorization: Bearer" -- Bearer is a
# dashboard session token and 401s a pt-sk-... key. Both prism.blockconvey.com
# and api.prism.blockconvey.com serve these endpoints; PRISM_ENDPOINT picks one.
# ---------------------------------------------------------------------------
def _headers() -> dict:
    return {"X-PRISMtrace-Key": config.PRISM_API_KEY, "Content-Type": "application/json"}


def _guardrail_payload(trace_id: str, text: str) -> dict:
    """project_id and messages are required. There is no `mode` field -- block
    vs flag is a property of the rule in the dashboard, not of the request.

    Only the LAST role:"user" message is evaluated, so the whole scoring window
    goes in as one user message; splitting it per speaker would hide the
    caller's ask on every window where the user happened to speak last.
    trace_id is optional and is what ties this decision to the trace sent next.
    """
    return {
        "project_id": config.PRISM_PROJECT,
        "trace_id": trace_id,
        "messages": [{"role": "user", "content": text}],
    }


def _trace_payload(trace_id: str, **kw) -> dict:
    """The local record. Richer than ingest accepts; _ingest_payload maps it."""
    return {"trace_id": trace_id, "project_id": config.PRISM_PROJECT,
            "timestamp": time.time(), **kw}


def _verdict_for_ingest(output: dict | str) -> str:
    """Serialize the verdict for output_message, minus the advisory prose.

    PRISM scans output_message against the project's rules at ingest, not just
    the input. Two of our own fields trip the project's rules:

    * user_action -- the sentence we generate FOR the victim ("do not give any
      part of your Social Security number") matches the read-back rule.
    * latency_ms -- scorer writes a full-precision perf_counter float, and
      PII/PHI Detection reads the digit run as a card or phone number
      ("851.0374200013757" -> "Phone Number: 0374200013757"). It is redundant
      here anyway; ingest takes latency_ms as a top-level int.

    Either one files a block-action flag against a trace where nothing was
    blocked. Dropping them keeps the Guardrails page to real detections. The
    full record, both fields included, stays in logs/traces.jsonl.
    """
    if not isinstance(output, dict):
        return output if isinstance(output, str) else json.dumps(output)
    drop = {"user_action", "latency_ms"}
    return json.dumps({k: v for k, v in output.items() if k not in drop})


def _ingest_payload(record: dict) -> dict:
    """Map the local record onto POST /api/traces.

    session_id is what groups traces into one trajectory; one call is one
    session, so it defaults to the call's trace_id. Fields ingest has no slot
    for (step, blocked, model_called, block_honoured, raw) ride under metadata,
    so the guardrail proofs survive the mapping.
    """
    output = record.get("output")
    blocked = bool(record.get("blocked"))
    # "raw" is the model's unparsed reply; it embeds user_action verbatim, so it
    # would re-introduce exactly what _verdict_for_ingest strips. Local log only.
    reserved = {"input", "output", "model", "latency_ms", "session_id", "project_id", "raw"}
    payload = {
        "project_id": config.PRISM_PROJECT,
        "session_id": record.get("session_id") or record.get("trace_id"),
        # Must be a real model name. The Traces list silently drops rows whose
        # model it does not recognise, so a literal "guardrail" here makes the
        # blocked run invisible in the console -- the block shows on the
        # Guardrails page and nowhere else. Send the model that WOULD have run;
        # metadata.model_called records that it did not. The Enforcement Check
        # does not read this field, so naming it does not affect the verdict.
        "model": record.get("model") or config.LLM_MODEL or "guardrail",
        "input_messages": [{"role": "user", "content": record.get("input", "")}],
        # We send spanless traces, and the Enforcement Check reads a spanless
        # trace that carries output as proof the model ran anyway
        # (output_after_block -> "Not honoured"). A blocked run produced no
        # model output, so it must ship none. The field is required, so "" is
        # the only way to say that; omitting it 422s. metadata and model are
        # NOT consulted by the check, so model_called/block_honoured below are
        # for our own log, not evidence PRISM reads.
        "output_message": "" if blocked else _verdict_for_ingest(output),
        # Validated as an int: a float 422s with "int_from_float". The
        # fractional milliseconds stay in the local log.
        "latency_ms": int(round(record.get("latency_ms") or 0)),
        "metadata": {k: v for k, v in record.items() if k not in reserved},
    }
    # trace_id is idempotent: re-sending one returns the EXISTING trace instead
    # of storing a new one. A call scores many windows, so sending the call id
    # every time would collapse them into the first trace. Send it only for the
    # guardrail-blocked record -- without it the Enforcement Check has nothing
    # to match and reports trace_not_found, which is not a pass -- and let the
    # rest group by session_id.
    if blocked and record.get("trace_id"):
        payload["trace_id"] = record["trace_id"]
    return payload


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
        # Every 200 carries `blocked` and `evaluated`; a block adds rule_name,
        # rule_type, matched_text and fallback_message. evaluated=false means no
        # rule actually ran (reason: plan_not_entitled / internal_error) and
        # PRISM fails open, so its blocked=false must NOT be read as "clean" --
        # that would silently disarm the detector on an entitlement lapse. Treat
        # it like an outage and use the local rules, same as the except below.
        if data.get("evaluated") is not True:
            local.raw = data
            _log_local({"kind": "guardrail", "trace_id": trace_id, "source": "local-not-evaluated",
                        "prism_reason": str(data.get("reason", "")), **asdict(local)})
            return local
        res = GuardrailResult(
            blocked=data.get("blocked") is True,
            reason=str(data.get("matched_text") or data.get("fallback_message") or ""),
            rule=str(data.get("rule_name") or data.get("rule_type") or ""),
            raw=data)
        _log_local({"kind": "guardrail", "trace_id": trace_id, "source": "prism", **asdict(res)})
        return res
    except Exception as e:  # noqa: BLE001
        _log_local({"kind": "guardrail", "trace_id": trace_id, "source": "local-fallback", "error": str(e), **asdict(local)})
        return local


async def send_trace(trace_id: str, *, step: str, input: str, output: dict | str,
                     latency_ms: float, blocked: bool, model: str = "",
                     session_id: str = "", extra: dict | None = None) -> None:
    record = _trace_payload(trace_id, step=step, input=input, output=output,
                            latency_ms=round(latency_ms, 1), blocked=blocked, model=model,
                            session_id=session_id or trace_id,
                            **(extra or {}))
    _log_local({"kind": "trace", **record})
    if not config.PRISM_ENDPOINT:
        return
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.post(f"{config.PRISM_ENDPOINT.rstrip('/')}/api/traces",
                                  headers=_headers(), json=_ingest_payload(record))
            r.raise_for_status()
    except Exception as e:  # noqa: BLE001
        # Logged, never raised: a dead PRISM must not take the detector with it.
        # Grep logs/traces.jsonl for "trace_error" when the dashboard is empty.
        _log_local({"kind": "trace_error", "trace_id": trace_id, "error": str(e)})
