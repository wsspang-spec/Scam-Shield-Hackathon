"""Replay sample transcripts through the scorer without audio or Twilio.

Usage:
  python scripts/replay.py                 # all samples, direct (no server)
  python scripts/replay.py samples/bank_scam.txt
  python scripts/replay.py --server http://localhost:8000 samples/bank_scam.txt   # via /simulate, drives the dashboard

Each run gets its own trace_id, so running all samples produces the 5 to 10
runs PRISM needs for Root Cause analysis.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def load(path: Path) -> list[str]:
    return [l.strip() for l in path.read_text().splitlines() if l.strip() and ":" in l]


async def run_direct(path: Path) -> None:
    from app import prism
    from app.scorer import CallState, Scorer

    alerts: list[dict] = []

    async def on_alert(r):
        alerts.append(r)

    async def on_event(ev):
        if ev["type"] == "score":
            fired = ", ".join(f"{f.get('class','?')[0].upper()}:{f['criterion'][:40]}" for f in ev.get("fired", []))
            print(f"    -> {ev['tier']:<9} {ev['score']:>3}  {ev.get('source','')[:9]:<9} {int(ev['latency_ms'])}ms  [{fired}]")
        elif ev["type"] == "turn":
            print(f"  [{ev['turn']}] {ev['speaker']}: {ev['text'][:90]}")

    state = CallState(trace_id=prism.new_trace_id(), metadata={"direction": "inbound", "saved_contact": "no"})
    scorer = Scorer(on_alert=on_alert, on_event=on_event)
    print(f"\n=== {path.name}  trace_id={state.trace_id}")
    for line in load(path):
        speaker, _, text = line.partition(":")
        await scorer.add_turn(state, speaker.strip().upper(), text)
    verdict = "ALERT FIRED" if alerts else "no alert"
    expected = "scam" in path.name
    ok = (bool(alerts) == expected)
    print(f"=== {verdict}  expected={'scam' if expected else 'legit'}  {'PASS' if ok else 'FAIL'}")


async def run_server(base: str, path: Path) -> None:
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(f"{base}/simulate", json={"lines": load(path)})
        data = r.json()
    print(f"=== {path.name} trace_id={data['trace_id']} alerted={data['alerted']}")
    for res in data["results"]:
        print(f"    {res['tier']:<9} {res['score']:>3} {res.get('source','')}")


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--server", default="")
    a = ap.parse_args()
    files = [Path(f) for f in a.files] or sorted((ROOT / "samples").glob("*.txt"))
    for f in files:
        if a.server:
            await run_server(a.server.rstrip("/"), f)
        else:
            await run_direct(f)


if __name__ == "__main__":
    asyncio.run(main())
