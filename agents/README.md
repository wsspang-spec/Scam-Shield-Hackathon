# Demo agents (ElevenLabs, Will's account)

| Persona | Agent ID | Expected result |
|---|---|---|
| Marcus, Chase fraud dept (scam) | `agent_4901m55ab5sdey7rbs1vmys2eyaq` | FRAUD, guardrail blocks at code read-back |
| Dana, Chase fraud prevention (legit twin) | `agent_3601m55af020ew4t08152es9p710` | stays SAFE or UNCERTAIN |

Paste an ID into the dashboard's agent field and click Answer call.
Both use the default voice (Eric) and DeepSeek Flash; swap the voice to a female
one for Dana if time allows so the two calls sound different.
