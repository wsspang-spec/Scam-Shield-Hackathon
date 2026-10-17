# Scam Shield: demo script (3 minutes)

## Setup before you walk up
- Dashboard open at localhost:8000, Marcus's agent ID in the field, mic allowed.
- Laptop volume up. Judges need to hear the caller.
- PRISM Guardrails page and Root Cause page open in two other tabs.
- Screen recording of a clean run saved on the desktop as the fallback.

## 0:00 The problem (20 seconds)
"Bank impersonation is the single largest imposter scam in America. $3.5 billion in
imposter losses last year, and the bank increasingly eats it under reimbursement
rules. Every fraud control a bank has runs on the bank's side of the call. Nobody
is on the customer's side. Scam Shield is."

## 0:20 The scam call (60 seconds)
Click Answer. Marcus speaks. You play along: "Yes, this is me." "No, I didn't buy
anything in Dallas." Let the score build. When he asks you to read the code back:

- Dashboard flips to FRAUD, guardrail blocks pre-model, the warning cuts him off,
  the session ends.
- Point at the screen: "It scored his behavior, not his vocabulary. 'Fraud
  department' and 'verify' are not evidence; a real bank says those words. The
  request to read back a code is. That is the PRISM guardrail firing before the
  model was ever called."
- Point at Fraud typology and Payment rail: "OTP interception. The rail he was
  steering toward was a wire to a 'secured account.' Typical completed loss for
  this archetype is $2,210."

## 1:20 The legitimate twin (40 seconds)
Paste Dana's ID. Answer. She greets you by name, asks you to confirm your zip and
date of birth before discussing the account, reads back two charges, blocks them,
closes the card, opens a dispute. This is how real outbound fraud calls run.

- Dashboard may go UNCERTAIN when she asks for zip and DOB. It must not go FRAUD.
  Legitimacy evidence fills in: yes/no on specific transactions, invites callback.
- "She asked for my date of birth. A real fraud agent does that before discussing
  the account, and so does a scammer. That is why real-time detectors lose
  precision, around 0.75 in the literature. We hold her at UNCERTAIN because
  authority and identity questions open a watch window, but only a request to
  supply a secret or move money can close it. She never made one."

## 2:00 PRISM proofs (45 seconds)
Switch tabs.
1. Guardrails page: "Here is the guardrail definition, block mode, and the run it
   stopped, under this trace ID."
2. Same trace: "Model not called, block honoured. PRISM agreed with the block."
3. Root Cause: "Five runs, three blocked. The cluster is credential read-back
   across bank, government and tech-support pretexts. Every scam archetype
   converges on the same extraction step regardless of the story. That is why the
   guardrail sits in front of the model."

## 2:45 Roadmap (15 seconds)
"Today the caller is an ElevenLabs agent and the transcript comes from the SDK. In
telephony mode, which is in the repo, a Twilio number fronts the customer's phone
and Scribe transcribes both legs. Same engine. A bank offers the protected number to
its highest-risk customers and the fraud desk sees the alert in real time."

## If asked
- Consent: inbound leg hears "this call may be monitored." 13 states need all-party
  consent. Nothing is stored except transcripts.
- Deepfakes: voice cloning changes the voice, not the script. We score the script.
- False positives: "Mark false positive" button logs to PRISM; that is the one
  in-product precision signal any shipping system has.
- Why not keywords: TF-IDF classifiers hit F1 0.95 on their own test set and
  collapse to 0.26 when vocabulary is controlled. We score speech acts.
