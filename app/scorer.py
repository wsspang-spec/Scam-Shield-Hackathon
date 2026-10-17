"""Rolling-window scam scorer.

Flow per committed CALLER (or USER) utterance:
  1. append turn
  2. PRISM guardrail on the recent window (block mode)
     -> blocked: tier FRAUD, fire intervention, no model call
  3. else: model call through Nicrron with the rubric -> JSON
  4. hysteresis: alert only after HYSTERESIS_WINDOWS consecutive FRAUD windows,
     or immediately on a dispositive item
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Awaitable, Callable

from openai import AsyncOpenAI

from . import config, prism
from .rubric import SYSTEM_PROMPT, build_user_message

AlertFn = Callable[[dict], Awaitable[None]]
EventFn = Callable[[dict], Awaitable[None]]


@dataclass
class CallState:
    trace_id: str
    turns: list[dict] = field(default_factory=list)
    summary: str = ""
    metadata: dict = field(default_factory=dict)
    scores: list[dict] = field(default_factory=list)
    consecutive_fraud: int = 0
    alerted: bool = False
    blocked_by_guardrail: bool = False


class Scorer:
    def __init__(self, on_alert: AlertFn, on_event: EventFn):
        self.on_alert = on_alert
        self.on_event = on_event
        self.client = AsyncOpenAI(base_url=config.NICRRON_BASE_URL, api_key=config.NICRRON_API_KEY or "missing")

    # -- public ---------------------------------------------------------------
    async def add_turn(self, state: CallState, speaker: str, text: str) -> dict | None:
        text = text.strip()
        if not text:
            return None
        turn = {"turn": len(state.turns) + 1, "speaker": speaker, "text": text, "ts": time.time()}
        state.turns.append(turn)
        await self.on_event({"type": "turn", **turn})
        if state.alerted:
            return None
        return await self.score(state)

    async def score(self, state: CallState) -> dict:
        window = state.turns[-config.WINDOW_TURNS:]
        window_text = "\n".join(f"{t['speaker']}: {t['text']}" for t in window)
        t0 = time.perf_counter()

        # 1. Guardrail before the model (PRISM proof 1)
        g = await prism.guardrail_evaluate(state.trace_id, window_text)
        if g.blocked:
            result = {
                "score": 100, "tier": "FRAUD", "archetype": "guardrail",
                "fired": [{"criterion": f"GUARDRAIL:{g.rule}", "class": "dispositive",
                           "quote": g.reason, "turn": window[-1]["turn"]}],
                "negatives": [], "user_action": "Hang up now. Call the number on the back of your card.",
                "source": "guardrail", "latency_ms": (time.perf_counter() - t0) * 1000,
            }
            state.blocked_by_guardrail = True
            # PRISM proof 2: same trace_id, model NOT called, block honoured
            await prism.send_trace(state.trace_id, step="score", input=window_text, output=result,
                                   latency_ms=result["latency_ms"], blocked=True,
                                   extra={"model_called": False, "block_honoured": True})
            await self._record(state, result)
            return result

        # 2. Model call through Nicrron
        user_msg = build_user_message(window, state.summary, state.metadata)
        raw = ""
        try:
            resp = await self.client.chat.completions.create(
                model=config.LLM_MODEL, temperature=0,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": user_msg}],
            )
            raw = resp.choices[0].message.content or ""
            result = _parse_json(raw)
        except Exception as e:  # noqa: BLE001
            result = {"score": 0, "tier": "UNCERTAIN", "fired": [], "negatives": [],
                      "archetype": "none", "user_action": "", "error": str(e)}
        result["source"] = "model"
        result["latency_ms"] = (time.perf_counter() - t0) * 1000
        result = _apply_tier_rules(result)

        await prism.send_trace(state.trace_id, step="score", input=user_msg, output=result,
                               latency_ms=result["latency_ms"], blocked=False, model=config.LLM_MODEL,
                               extra={"model_called": True, "raw": raw[:2000]})
        await self._record(state, result)
        return result

    # -- internals ------------------------------------------------------------
    async def _record(self, state: CallState, result: dict) -> None:
        state.scores.append(result)
        await self.on_event({"type": "score", "trace_id": state.trace_id, **result})

        dispositive = any(f.get("class") == "dispositive" for f in result.get("fired", []))
        if result["tier"] == "FRAUD":
            state.consecutive_fraud += 1
        else:
            state.consecutive_fraud = 0

        should_alert = (
            not state.alerted
            and (dispositive or state.consecutive_fraud >= config.HYSTERESIS_WINDOWS)
        )
        if should_alert:
            state.alerted = True
            await self.on_alert({"trace_id": state.trace_id, **result})


def _parse_json(raw: str) -> dict:
    s = raw.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.S)
    start, end = s.find("{"), s.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON in model output: {raw[:200]}")
    data = json.loads(s[start:end + 1])
    data.setdefault("fired", [])
    data.setdefault("negatives", [])
    data.setdefault("user_action", "")
    data.setdefault("archetype", "none")
    data["score"] = int(data.get("score", 0))
    return data


def _apply_tier_rules(r: dict) -> dict:
    """Enforce the tier logic in code so the model cannot drift."""
    classes = {f.get("class") for f in r.get("fired", [])}
    score = r["score"]
    if score >= config.FRAUD_THRESHOLD:
        tier = "FRAUD"
    elif score >= config.UNCERTAIN_THRESHOLD:
        tier = "UNCERTAIN"
    else:
        tier = "SAFE"
    if "dispositive" in classes and "strong" in classes:
        tier = "FRAUD"
    # cap at UNCERTAIN until a request directed at the user has fired
    if tier == "FRAUD" and not (classes & {"dispositive", "strong"}):
        tier = "UNCERTAIN"
    r["tier"] = tier
    return r
