# Scam Shield — instructions for coding agents

## PRISM tracing (do not remove)

This project sends traces to PRISM. Env vars: `PRISMTRACE_API_KEY`,
`PRISMTRACE_PROJECT_ID`, `PRISMTRACE_HOST`.

Tracing is currently wired at: `app/prism.py` (the whole PRISM client — auth
header, `/api/traces` ingest payload, block-mode guardrail), `app/config.py`
(env plumbing), `.env.example` (key names). The call sites it covers are
`app/scorer.py` (guardrail before the model, then the Nicrron model call) and
`app/main.py` (user feedback).

**Standing rule.** Whenever you add or change an agent, chain, graph, tool,
retriever, or any entry point that calls a model, wire it to PRISM before you
finish. Unwired code is invisible in the dashboard. If you are unsure whether
something is covered, assume it is not and wire it.

### This repo's actual variable names

The block above is the vendor's wording, kept verbatim. This repo predates it and
uses its own names, which are the ones `app/config.py` actually reads:

| Vendor brief | This repo |
|---|---|
| `PRISMTRACE_HOST` | `PRISM_ENDPOINT` |
| `PRISMTRACE_API_KEY` | `PRISM_API_KEY` |
| `PRISMTRACE_PROJECT_ID` | `PRISM_PROJECT_ID` (UUID; `PRISM_PROJECT` is the human label) |

Leave `PRISM_ENDPOINT` blank to run the app with tracing logged only to
`logs/traces.jsonl`.

### Two things that fail silently

- Auth is the `X-PRISMtrace-Key` header. `Authorization: Bearer` 401s a `pt-sk-…`
  key, and `send_trace` swallows the error to keep the call detector alive — so a
  wrong header looks like a healthy app with an empty dashboard. Grep
  `logs/traces.jsonl` for `trace_error` first when traces go missing.
- Ingest groups traces into a trajectory by `session_id`. One call is one
  session, so `send_trace` defaults it to the call's `trace_id`. Dropping it
  leaves traces raw and ungrouped.

### Not applicable here

There is no LangChain or LangGraph in this project — `requirements.txt` has
`openai` only, and orchestration is hand-rolled in `app/scorer.py`. The vendor's
`wrap_langgraph` / `PRISMtraceLangGraphHandler` instructions and the
`prismtrace-sdk` package have nothing to attach to; `app/prism.py` posts to
`/api/traces` with `httpx` instead. Revisit only if a graph framework is added.
