# Scam Shield

Real-time scam call interception. A Twilio number sits in front of your real phone,
transcribes both sides of the call with ElevenLabs Scribe, scores the caller's
behavior every turn (PRISM guardrail first, then an LLM through Nicrron), and when
the score crosses the line it plays a warning into your ear and drops the caller.

Built for Money Talks 2 (Block Convey), Trust & Risk track.

```
Scammer --> Twilio number --> Conference <-- your phone (server dials you in)
                                 |
            Media Stream (both tracks, mu-law 8k) --> /media websocket
                                 |
             ElevenLabs Scribe v2 Realtime (one session per track)
                                 |
   rolling window --> PRISM guardrail (block mode) --> blocked? warn + kick caller
                                 |  not blocked
                     Nicrron LLM + rubric --> score, tier, fired criteria
                                 |
                      dashboard (live transcript, gauge, criteria)
```

## Why it works

The research behind the rubric is in `docs/research.md`. Short version: scam calls
and legitimate calls use the same vocabulary (fraud department, verify, urgent). What
separates them is the **direction of information flow and the exit path**. Scammers
ask you to supply secrets (read back a code, PIN, SSN) or move money on irreversible
rails (gift cards, crypto kiosk, wire to a "safe account"), and they will not let you
hang up and call back. Legitimate banks confirm data they already hold with yes/no
questions and invite you to call the number on your card. The guardrail encodes the
dispositive signals; the model handles the gray zone.

## Two ways to run a call

**Browser demo mode (default for the hackathon).** An ElevenLabs Conversational AI
agent plays the caller; you talk from the laptop mic. The dashboard at `/` has
"Answer call." Transcript events from the agent SDK feed the scorer directly, so
nothing in the detection path changes. On alert the page mutes the agent, plays
the warning, and ends the session. Set up two agents from `agents/scammer_agent.md`
and `agents/legit_agent.md`, paste the agent ID into the dashboard, click Answer.
No Twilio needed.

**Telephony mode (roadmap, code included).** A Twilio number fronts your real phone,
Scribe transcribes both legs from the media stream, same scorer, warning injected
into your leg via conference announce. Requires a paid Twilio number. See Setup.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in keys
ngrok http 8000        # put the host (no https://) in PUBLIC_HOST
uvicorn app.main:app --reload --port 8000
```

Twilio console: set your number's Voice webhook to `https://<PUBLIC_HOST>/twilio/inbound` (POST).

Optional: `python scripts/make_warning.py` generates the warning clip with ElevenLabs TTS.

## Test without a phone

```bash
python scripts/replay.py                       # all samples, prints per-turn scores, PASS/FAIL
python scripts/replay.py samples/bank_scam.txt
python scripts/replay.py --server http://localhost:8000 samples/bank_scam.txt   # drives the dashboard at /
```

`samples/` holds three scam scripts and two legitimate twins. The legit twins are the
hard negatives: a real bank fraud call and a real collections call. They must stay
below the alert line.

## Demo flow

1. Open the dashboard at `https://<PUBLIC_HOST>/`.
2. Have the "scammer" (ElevenLabs agent per `agents/scammer_agent.md`, or a teammate
   reading `samples/bank_scam.txt`) call the Twilio number.
3. Your phone rings, answer. Judges watch the dashboard. Transcript streams, score
   climbs, criteria light up with the caller's exact words.
4. At the code read-back request the guardrail blocks, the warning plays in your ear,
   the caller is removed five seconds later.
5. Repeat with `bank_legit.txt` to show it stays SAFE/UNCERTAIN.
6. Fallback if telephony dies: `scripts/replay.py --server` drives the same dashboard
   from text.

## PRISM proofs (Trust & Risk)

All PRISM calls live in `app/prism.py`. Adjust the two payload functions to the docs.

1. **Guardrail (block mode, before the model).** `guardrail_evaluate()` is called on
   every window before any model call, with the call's `trace_id`. Guardrail
   definition to author in PRISM, same intent as the local fallback rules:

   > Block when the CALLER asks the USER to read back, text or type a one-time code,
   > PIN, password, CVV, full card number or SSN; directs payment via gift card,
   > crypto kiosk, wire to a new or "safe" account, cash or gold courier, or
   > "send money to yourself"; or instructs secrecy from the bank or family.
   > Also block when the USER begins reciting a card number or SSN.

   Show it blocking on `bank_scam.txt` turn 5 ("read that code back to me").

2. **Block check.** `send_trace()` sends the run under the same `trace_id` with
   `model_called=false, block_honoured=true`. On the Guardrails page, show the block
   as honoured and say whether PRISM agreed.

3. **Root cause.** Run `python scripts/replay.py` once; it produces five runs (three
   blocked). Analyse them, then Root Cause -> Analyze now. Expected cluster:
   "credential read-back request" across bank, SSA and tech-support archetypes.
   One-sentence cause: every archetype converges on the same extraction step
   regardless of pretext, so the guardrail catches it before the model.

Local copies of every guardrail decision and trace are in `logs/traces.jsonl`.

## Model calls

All model calls go through `NICRRON_BASE_URL` (OpenAI-compatible) using
`LLM_MODEL`. Change the model in `.env`, nothing else.

## Known limits

- Scribe realtime param names (`audio_format`, `sample_rate`) are the only thing in
  `app/transcriber.py` to verify against docs. Both are isolated in `_url()` and
  `_chunk_msg()`.
- Conference participant announce plays to the user leg only; verify
  `announce_url` in the Twilio docs if the warning does not play.
- Consent: the inbound leg hears "This call may be monitored for fraud protection."
  Thirteen US states require all-party consent for recording; nothing is stored
  except transcripts in `logs/`.

## Roadmap

Same engine, different audio source: carrier SIP trunk or on-device call audio.
Add STIR/SHAKEN attestation and claimed-institution vs. number mismatch as metadata
inputs (already a rubric line, not yet wired).
