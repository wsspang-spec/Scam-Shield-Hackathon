# Demo agents (ElevenLabs, Will's account)

| Persona | Agent ID | Expected result |
|---|---|---|
| Marcus, Chase fraud dept (scam) | `agent_4901m55ab5sdey7rbs1vmys2eyaq` | FRAUD, guardrail blocks at code read-back |
| Dana, Chase fraud prevention (legit twin) | `agent_3601m55af020ew4t08152es9p710` | stays SAFE or UNCERTAIN (voice: Ms. Walker) |

| Chase official line (callback verification) | `agent_7001m55g956kfsxvdsqcngxkpy3j` | confirms FR229471, denies anything else |

Paste a caller ID into the dashboard's agent field and click Answer call. The
bank-line ID is prefilled; the shield calls it automatically after a caller gives
a reference number.
