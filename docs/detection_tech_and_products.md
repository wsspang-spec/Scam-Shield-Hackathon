# Real-time scam call detection: products, technical work, signals, and gaps

Research date: 2026-10-17. Scope: how shipping products and recent papers detect scam calls in real time from audio/transcript, what signals they use, published metrics, failure modes, and open gaps a hackathon prototype could claim.

## Q1. How do Google Pixel Scam Detection, Samsung/Hiya, Apple iOS 26 Call Screening, Truecaller AI Call Scanner, and carrier offerings work, and do any analyze conversation content in real time?

### Takeaway
Only two consumer products actually analyze live conversation content: Google's Pixel Scam Detection (on-device Gemini Nano, flags "conversation patterns," opt-in, audible beep to the other party) and Hiya AI Phone (analyzes call audio for scam language plus AI-voice detection). Truecaller's AI Call Scanner is a voice-clone detector triggered manually, Apple's Call Screening is a pre-answer gatekeeper (transcribes caller's stated reason, no scam classification), and carriers (T-Mobile, AT&T, Verizon) work purely on network metadata and STIR/SHAKEN, never on content.

### Cited Findings

**Google Pixel Scam Detection (Phone by Google)**
- Launched as public beta Nov 2024 for English-speaking US users on Pixel 6+. On Pixel 9 it is powered by Gemini Nano; Pixel 6-8 use unnamed "other on-device machine learning models." It analyzes "conversation patterns" to spot tactics such as "urgent requests for fund transfers due to alleged account breaches." Alert is audio + haptic + visual. Off by default. "No conversation audio or transcriptions are stored on the device, sent to Google servers, or accessible after the call." — [Help Net Security](https://www.helpnetsecurity.com/2024/11/14/android-scam-detection/)
- Stable release in the March 2025 Pixel Drop. Example patterns it watches for: someone posing as a bank representative urgently asking for fund transfers, gift card payments, or PINs/passwords. UI: phone vibrates and makes noise, then shows "Suspicious activity detected for this call" with "End call" and "Not a scam" buttons. Google Messages got parallel on-device ML scam-text classification, initially for package-delivery and job scams, auto-moving hits to "Spam & blocked." — [9to5Google](https://9to5google.com/2025/02/26/pixel-scam-detection-messages-phone/)
- Official support page: "A beep plays at the start of the call and every few minutes after, so participants know the feature is on." Can be turned off per call via More > Scam Detection. Processing is "entirely on the device." Regions: Pixel 6+ in US; Pixel 9+ in Australia, Canada, France, Germany, India, Ireland, Italy, Japan, Mexico, Singapore, Spain, UK; SIM must match country and device must be in that country. Stated limitations: "Not all scam calls can be detected," "isn't 100% accurate." — [Google Phone app help: Use Scam Detection](https://support.google.com/phoneapp/answer/15654065?hl=en)
- May 2025: Google expanded Messages scam detection to toll/billing fee, crypto, financial impersonation, gift card/prize, and tech support scams; Chrome 137 desktop uses Gemini Nano to evaluate pages for tech-support-scam signals (e.g., keyboard lock API use). Google is piloting in-call screen-sharing warnings with UK banks Monzo, NatWest, and Revolut: if a participating banking app is opened during screen sharing with an unknown contact, the user is warned (Android 11+). — [The Hacker News](https://thehackernews.com/2025/05/google-rolls-out-on-device-ai.html)
- Gap in the public record: Google has never published precision/recall, latency to first alert, or how many utterances are needed. No source found states whether saved contacts are excluded.

**Hiya and Samsung Smart Call**
- Hiya and Samsung extended their partnership through 2028; Hiya powers Samsung Smart Call "helping stop spam and fraud calls" on "hundreds of millions of Samsung devices globally." The announcement gives no detection-signal details for Smart Call itself. — [BusinessWire, Jan 28 2025](https://www.businesswire.com/news/home/20250128511230/en)
- Hiya AI Phone (separate app, iOS and Android) "analyzes call audio for scam language and other indicators" in real time and detects AI-generated or AI-modified voices "by looking for subtle audio patterns" (deep-learning capability from Hiya's summer 2024 acquisition of Loccus.ai). UX: phone vibrates and shows an on-screen warning. On-device vs cloud is not stated; Hiya says it doesn't store personal or call data on its servers without consent. Hiya cites a Censuswide survey (2,000 US consumers, Jan 2025): 1 in 3 Americans received a deepfake scam call in 2024; 34% of those targeted lost an average of $7,200. — [BusinessWire](https://www.businesswire.com/news/home/20250128511230/en)
- Historical Smart Call behavior: Hiya's cloud database and service identify suspicious calls; starting with One UI 2.5 Smart Call automatically blocks fraud calls (previously only labeled). — [Hiya blog (2020)](https://blog.hiya.com/hiya-samsung-extend-strategic-partnership-to-2025)

**Apple iOS 26 Call Screening and Hold Assist**
- Apple: "Call Screening responds to potential spam calls, automatically answering unknown numbers on your behalf," ringing you only if the call is legitimate. "Hold Assist detects hold music and stays on the line for you." Messages: "Unknown senders will require approval" unless time-sensitive (e.g., verification codes). Apple did not state whether Call Screening runs on-device (it did say Live Translation does). — [Jamf WWDC25 recap](https://www.jamf.com/blog/apple-wwdc2025-keynote-recap/)
- Mechanics: an automated voice asks unknown callers for name and reason; the response is shown as a text transcription and the user accepts/rejects. Known contacts are not screened. Settings > Apps > Phone > Unknown Callers: Never / Ask Reason for Calling / Silence. Works on iPhone 11 onward, does not require Apple Intelligence. Reported issues: users missing important calls; requests for clearer alerts that screening is active. It screens on the caller's stated reason, not on scam content analysis. — [TechRadar](https://www.techradar.com/phones/iphone/call-screening-in-ios-26-has-finally-ended-my-spam-call-nightmare-heres-how-to-set-it-up)

**Truecaller AI Call Scanner**
- Launched May 2024, Android first, US first, part of Premium. User taps a dedicated button during a suspicious call; the caller's voice is recorded and sent for analysis by "an advanced AI model trained to identify the unique characteristics of human speech" vs AI-generated voices. Result in "just a few seconds" with "a high degree of accuracy"; no accuracy figures, sample length, or storage policy published. Truecaller plans to adapt to new voice synthesis methods and considered a chatbot for forwarded clips. — [Help Net Security](https://www.helpnetsecurity.com/2024/05/29/truecaller-ai-call-scanner/); corporate release: [Inderes/Truecaller AB](https://inderes.fi/releases/truecaller-ab-truecaller-launches-the-worlds-first-ai-cloned-voice-detection)
- Note: this is a voice-liveness check, not conversation-content analysis, and it is user-initiated rather than continuous.

**Carriers**
- T-Mobile Scam Shield: uses network data and machine learning to identify spoofing and robo-dialers; labels calls "Scam Likely"; the article says it "primarily relies on the STIR/SHAKEN caller ID protocol." Text reports to 7726 feed a shared security database. Free tier: Scam ID, Scam Block, Caller ID, Scam Reporting, Callback Protection; Premium ($4/line) adds category blocking, reverse lookup, voicemail-to-text. User complaints include false positives causing missed legitimate calls. — [SlashGear](https://www.slashgear.com/2200747/tmobile-report-spam-feature-effectiveness/); product page: [T-Mobile Scam Shield](https://www.t-mobile.com/scamshield)
- AT&T network analytics (basis of Call Protect / ActiveArmor): identifies robocallers via call patterns, e.g., "multiple short-duration calls to numbers on the National Do Not Call list"; AT&T staff review a daily list to avoid suspending legitimate automated callers such as school districts. ActiveArmor automatically blocks fraud calls and labels nuisance calls; auto-enabled for eligible HD Voice lines. (Page dated 2017.) — [AT&T](https://www.att.com/es-us/sdabout/pages/cyberaware/ni/robocall)
- Verizon Call Filter: press material claims protection of 80M+ customers from 20B+ unwanted calls; no signal detail found in the fetched results. — [Verizon](https://espanol2.verizon.com/about/node/923075)

### Inferences
- The market splits into three layers that rarely combine in one product: (1) pre-call metadata/reputation (carriers, Hiya Connect, Truecaller caller ID), (2) pre-answer gatekeeping (Apple Call Screening, Google Call Screen), (3) in-call content analysis (Pixel Scam Detection, Hiya AI Phone). Only Google and Hiya do layer 3, and neither publishes metrics.
- Google's design choices (opt-in, off by default, on-device, audible beep every few minutes, per-call kill switch, "Not a scam" feedback button) are effectively the de facto UX and legal template for in-call content analysis.
- Apple's approach shows that the "explain why you're calling" transcript is itself a cheap, high-signal pre-call input that a prototype could feed into an LLM classifier.

### Gaps
- No published precision/recall/latency for Pixel Scam Detection, Hiya AI Phone, or Truecaller AI Call Scanner.
- No primary source found specifying whether Pixel Scam Detection excludes saved contacts, or how many seconds/utterances before first alert.
- Apple has not disclosed whether Call Screening transcription is on-device.
- Verizon Call Filter and AT&T ActiveArmor current (2024-26) signal sets not found in primary sources; only old (2017) AT&T detail.

## Q2. What do academic/industry papers describe for LLM/NLP scam-call classification from transcripts (prompts, rubrics, features, accuracy)?

### Takeaway
Papers consistently show that off-the-shelf LLMs reach very high recall (0.98-1.00) on scam transcripts but suffer precision problems in real-time/turn-by-turn settings (0.70-0.77 on hard negatives), and that the main levers are (a) adding an "UNCERTAIN" class, (b) explicit expert-written criteria in the prompt, (c) block/turn-level scoring averaged over the call, and (d) retrieval of similar past snippets. Datasets are small, mostly Korean/Chinese/Turkish, and almost all evaluations are post-hoc rather than streaming.

### Cited Findings

**"It Warned Me Just at the Right Moment": LLM-based real-time phone scam detection (arXiv 2502.03964, Feb 2025)**
- Detector runs after each speaker turn on ASR text with conversation history. Two prompts: RT (output FRAUD or SAFE) and UNC (adds UNCERTAIN when info insufficient). Models: GPT-4, GPT-4o, GLM4, Doubao-Pro-32k, ERNIE-3.5-8k. Data: Chinese real scam/normal calls transcribed from public video platforms (e.g., YouTube) plus synthetic dialogues seeded with suspicious keywords; dataset sizes not reported. — [arXiv HTML](https://arxiv.org/html/2502.03964v1)
- Results: RT recall 0.98-1.00 across models; RT precision on synthetic hard negatives 0.70-0.77 for most models vs 0.95-1.00 for retrospective (whole-call) analysis. UNC prompt raised precision (Doubao 0.70 to 0.83, ERNIE 0.70 to 0.85) but lowered recall to 0.90-0.98 and delayed alerts (police-impersonation call flagged at utterance 6 under RT vs utterance 10 under UNC). — [arXiv HTML](https://arxiv.org/html/2502.03964v1)
- False-positive categories: legitimate identity verification, legitimate financial information sharing, legitimate urgent decision-making. Example: a flight re-booking call flagged at utterance 15 because the agent said "payment" about a modification fee. No latency measurements, no user study (despite the title), ASR engine not named. — [arXiv HTML](https://arxiv.org/html/2502.03964v1); version check: only v1 exists as of fetch — [arXiv abs](https://arxiv.org/abs/2502.03964)

**Fine-tuning small LMs for Korean voice phishing (arXiv 2506.06180, June 2025)**
- Two-stage pipeline: split transcript into fixed-length letter blocks (500 letters in training; 100-2,500 tested), LM scores each block 0-10 for VP likelihood, then a block-length-weighted average is compared to a threshold tuned on validation. Prompt variants: Plain, Cri (11 expert-written VP criteria), CoT, CoTCri. Model: Llama-3-Korean-Bllossom-8B with LoRA rank 8, 8-bit, 5 epochs; GPT-4o used as teacher labeler. Dataset: 1,377 Korean transcripts (219 real VP from Financial Supervisory Service/KBS + 35 hand-written synthetic VP; 1,158 non-VP incl. 58 "confusable" adversarial transcripts). — [arXiv HTML](https://arxiv.org/html/2506.06180v1)
- Results (accuracy only): normal test set, GPT-4o and Llama3-FT-Cri up to 100%, KoBERT 98.52%. Adversarial set: GPT-4o-Cri 99.11%, Llama3-FT-Cri 94.64%, KoBERT collapses to 56.25%. CoT hurt or did not help the 8B model. Not evaluated for streaming/early detection; authors note ChatGPT-generated scam dialogue was unrealistic and transcripts were manually corrected (so ASR noise is untested). — [arXiv HTML](https://arxiv.org/html/2506.06180v1)

**Korean Voice Phishing Benchmark (LREC 2026)**
- 160 dialogues (80 VP derived from 94 Financial Supervisory Service audio files 2015-2023, filtered to institutional impersonation with >7 turns; 80 general finance/insurance call-center dialogues from AI Hub). Four tasks: T1 whole-conversation yes/no, T2 topic classification, T3 dialogue structure recognition, T4 speaker identification. 14 open-source models tested (Bllossom 253B/70B/8B/3B, Gemma-3 27B to 270M, Llama-3.1-8B, Llama-3.2-3B, Qwen2.5-72B/7B, Qwen3-4B). T1 accuracy: Qwen2.5-72B 97.5%, Gemma-3-27B 90.6%, Gemma-3-1B 38.1%, Gemma-3-270M 49.4%. T2 topped out around 52.5%; T3 Boundary F1 best 34.99. Authors: detection "requires contextual reasoning and dialogue structure understanding, not just sentence-level comprehension"; evaluation is post-hoc, "does not test real-time detection or continuous monitoring"; text-only omits intonation/emotion. — [ACL Anthology PDF](https://aclanthology.org/2026.lrec-1.585.pdf); [listing](https://aclanthology.org/2026.lrec-1.585/)

**Turkish phone scams, audio vs transcript with multimodal LLMs (arXiv 2606.24523, poster, 2026)**
- 100 Turkish YouTube calls (50 scam, 50 benign). Raw 16 kHz audio fed directly to Gemini 2.5 Flash/Flash-Lite/Pro, GPT-4o, Qwen Max/Plus/Turbo vs transcripts from ElevenLabs Scribe V1 (with and without human correction). Mean F1: ~0.97 raw audio, 0.99 uncorrected transcripts, 0.99-0.995 corrected. Corrected vs uncorrected ASR differed by only ~0.008 F1, so ASR quality barely mattered. Main audio failure mode: safety-filter refusals on calls with profanity, intimidation, police impersonation (counted as false negatives); authors suspect vocal aggression triggers filters that text does not. — [arXiv PDF](https://arxiv.org/pdf/2606.24523)

**ConvoSentinel / SEConvo: chat-based social engineering detection (arXiv 2406.12263, 2024)**
- SEConvo: 1,400 GPT-4-Turbo-generated conversations (academic collaboration, funding, journalism, recruitment); 400 human-annotated (macro F1 0.91 agreement with intended labels). Target agents were deceived in >90% of clearly malicious conversations. Zero/few-shot detection: GPT-4-Turbo two-shot macro F1 0.78; Llama2-7B 0.67. — [arXiv HTML](https://arxiv.org/html/2406.12263v2)
- ConvoSentinel pipeline: (1) message-level sensitive-information-request detector (fine-tuned Flan-T5-Large, F1 0.89), (2) RAG snippet-level intent judge retrieving similar 3-turn snippets, (3) conversation-level aggregator. Macro F1 0.80 (GPT-4-Turbo) vs 0.78 two-shot; 0.73 (Llama2-7B) vs 0.67; ~61.5% fewer prompt tokens; F1 0.74 at just five messages (earlier detection). — [arXiv HTML](https://arxiv.org/html/2406.12263v2)

**Other 2025 work surfaced (not fully read)**
- RAG-based LLM real-time fraud detection (arXiv 2501.15290) — [arXiv](https://arxiv.org/pdf/2501.15290). Content not verified in this pass.

### Inferences
- A practical prompt rubric emerges from these papers: an explicit list of scam criteria (impersonation of authority, urgency, request for money transfer/gift cards/crypto, request for PIN/OTP/password, secrecy/isolation, threat of arrest or account closure), a three-way FRAUD/UNCERTAIN/SAFE output, a 0-10 score per window, and temporal aggregation (weighted average or hysteresis) rather than firing on a single utterance.
- Hard negatives are the real test: legitimate bank fraud-department calls, airline rebooking, and customer-service identity checks produce the same lexical triggers. Any prototype demo should include these to be credible.
- ASR errors matter less than expected (Turkish study), so a hackathon can lean on a commercial streaming ASR without heavy post-correction.
- Text beats raw audio for LLM classification partly because safety filters refuse aggressive audio; a prototype should classify on transcript and treat audio as a separate liveness/prosody channel.

### Gaps
- No paper found that measures end-to-end latency (audio in to alert out) or utterance-to-first-alert on a real streaming pipeline.
- No English-language real-call dataset found; the real-call corpora are Chinese, Korean, Turkish, or synthetic English chat.
- No controlled user study found on alert timing, trust, or alert fatigue for in-call scam warnings (the 2502.03964 title suggests one but the paper has none).
- 2501.15290 (RAG fraud detection) not read; its claims are unverified here.

## Q3. What acoustic/voice signals matter: synthetic voice/deepfake detection, VoIP/call-center noise, spoofed caller ID, STIR/SHAKEN?

### Takeaway
Commercial deepfake detectors (Pindrop, Reality Defender, Hiya/Loccus, Truecaller) market "real or AI" liveness on live calls but publish almost no methodology; ElevenLabs' own classifier is only for ElevenLabs audio (99% precision / 80% recall unmodified). STIR/SHAKEN attestation (A/B/C) is the standard caller-ID-trust signal and is already the primary input for carrier "Scam Likely" labels.

### Cited Findings
- Pindrop Pulse "Detects deepfakes, synthetic video and voices, and AI agents in real time"; marketing claims "Independently validated at 99% accuracy" (meta description; no methodology in body), "2300+ detection signals," 2.7M known bad actors, BotStopper tells human from machine "in about two seconds" and "matches against 5000+ AI voices." CCaaS integrations: Verizon, Genesys, Five9, Amazon Connect, Cisco, NICE. No false-positive rate or latency for Pulse disclosed. — [Pindrop Liveness Detection](https://pindrop.com/products/liveness-detection)
- Reality Defender RealCall: "real-or-AI answer on live calls," no voice enrollment, returns an "uncertain" result when audio cannot support a clear answer; results route callers to self-service/verification/agent/exit; combinable with voice biometrics, device, and account signals; enterprise only; bank case study cites ~600 reps across 1.7M+ calls but no accuracy. — [Reality Defender RealCall](https://www.realitydefender.com/product/realcall)
- ElevenLabs Audio Detector checks for ElevenLabs' imperceptible watermark and falls back to the legacy AI Speech Classifier, which is "99% precision, 80% recall" on unmodified ElevenLabs audio only; it does not detect other vendors' audio, third-party models served via ElevenLabs are generally not watermarked, and it is UI-only (no API documented). — [ElevenLabs docs: Audio detector](https://elevenlabs.io/docs/eleven-creative/audio-tools/audio-detector)
- Truecaller AI Call Scanner: human-vs-AI voice classification from a recorded sample of the caller, results in seconds, no metrics published. — [Help Net Security](https://www.helpnetsecurity.com/2024/05/29/truecaller-ai-call-scanner/)
- Hiya AI Phone: AI-voice detection via "subtle audio patterns," deep learning from Loccus.ai acquisition. — [BusinessWire](https://www.businesswire.com/news/home/20250128511230/en)
- Multimodal LLMs on raw call audio: F1 ~0.97 but refusals on aggressive audio; models "may also struggle with overlapping speech and background noise." — [arXiv 2606.24523](https://arxiv.org/pdf/2606.24523)
- STIR/SHAKEN attestation: A (Full) = provider originated the call on its IP network, knows the customer, and verified the number association ("This is my customer. I gave them this telephone number"); B (Partial) = knows the customer but has not verified number ownership; C (Gateway) = no relationship to originator, e.g., international gateway. A is "lowest risk"; calls below A "risk being marked as spam or blocked by the terminating provider"; attestation is increasingly an input to robocall analytics. It is a provider-to-number relationship signal and does not verify intent. — [TransUnion](https://www.transunion.com/blog/what-are-the-attestation-levels-for-stir-shaken)
- T-Mobile Scam Shield "primarily relies on the STIR/SHAKEN caller ID protocol" plus network ML for spoofing and robo-dialers. — [SlashGear](https://www.slashgear.com/2200747/tmobile-report-spam-feature-effectiveness/)

### Inferences
- For a prototype, synthetic-voice detection is the weakest link to build from scratch: there is no public API with disclosed accuracy for arbitrary TTS, and ElevenLabs' classifier only covers ElevenLabs. A hackathon should treat voice-liveness as an optional, clearly-labeled "experimental" signal or call a vendor API, and lead with transcript-based intent detection.
- STIR/SHAKEN attestation is not exposed to third-party apps on the handset; it lives at the carrier/analytics layer. A prototype that runs on a VoIP line (e.g., Twilio) can read SIP Identity headers, but a consumer phone app cannot.
- Background-noise and call-center acoustics appear in vendor marketing but no published study quantified them as discriminative features in the sources found.

### Gaps
- No peer-reviewed or vendor-published false-positive rates for Pindrop Pulse, RealCall, Hiya, or Truecaller liveness on live telephony audio.
- No source found quantifying VoIP/call-center background acoustics or codec artifacts as scam signals.
- No handset-level API found that exposes STIR/SHAKEN verstat to third-party apps (not confirmed either way in this pass).

## Q4. What metadata signals matter: number reputation, call frequency, international origin, spoofing of a bank's real number?

### Takeaway
Carrier and analytics vendors score calls on volume/velocity, short-duration call patterns, Do-Not-Call list hits, consumer reports, recycled-number history, and STIR/SHAKEN attestation; the same signals generate well-documented false positives for legitimate high-volume callers, and spoofing of a real institution's number is handled at the attestation layer rather than by handset apps.

### Cited Findings
- AT&T robocall analytics flag "multiple short-duration calls to numbers on the National Do Not Call list"; humans review daily to avoid blocking legitimate automated callers such as school districts. — [AT&T](https://www.att.com/es-us/sdabout/pages/cyberaware/ni/robocall)
- Factors that get a number labeled "Scam Likely": frequency and timing of calls (unusually many in a short period), known scam signatures (pre-recorded messages, requests for personal information, aggressive sales tactics), accidental inclusion in automated dialer campaigns, previous owner's activity on a recycled number, and algorithm false positives including caller-ID spoofing by others. Remediation: contact provider with call records; label removal "can be slow." — [BrightCall](https://www.brightcall.ai/blog/why-does-my-number-show-up-as-scam-likely)
- Attestation level C covers international-gateway calls where the provider cannot vouch for the originator; A attestation is tied to Branded Call Display and higher answer rates. — [TransUnion](https://www.transunion.com/blog/what-are-the-attestation-levels-for-stir-shaken)
- T-Mobile's 7726 report database is shared across carriers and used to tune filters, possibly ML training. — [SlashGear](https://www.slashgear.com/2200747/tmobile-report-spam-feature-effectiveness/)
- Google's bank pilot (Monzo, NatWest, Revolut) uses a behavioral signal rather than number reputation: opening a banking app while screen-sharing during a call with an unknown contact triggers a warning. — [The Hacker News](https://thehackernews.com/2025/05/google-rolls-out-on-device-ai.html)

### Inferences
- Number reputation is a commodity (Hiya, Truecaller, carriers) and a prototype cannot out-do it; the differentiating move is to combine reputation (is this number in contacts / does it claim to be a bank) with transcript intent ("I'm calling from your bank's fraud department").
- The "spoofed bank number" case is specifically where metadata fails and content analysis is needed: a spoofed A-attested number looks legitimate, but the conversation still contains the scam script.

### Gaps
- No primary 2024-26 source found enumerating Hiya's or First Orion's exact feature set (the "Adaptive AI" details were not in the fetched pages).
- No public statistics found on how often bank numbers are spoofed with successful STIR/SHAKEN attestation.

## Q5. What are documented false-positive problems and UX/privacy/consent concerns?

### Takeaway
Documented false-positive modes are (a) legitimate calls that share scam vocabulary (identity verification, payments, urgency) in content-based systems and (b) legitimate high-volume callers mislabeled "Scam Likely" in metadata systems; the privacy/legal template is Google's: on-device, opt-in, nothing stored, audible beep to all parties. Thirteen US states require all-party consent to record, and the law does not clearly say whether unstored real-time transcription counts as recording.

### Cited Findings
- Content-based FPs: legitimate identity verification, financial info sharing, urgent decision-making; flight rebooking call flagged on the word "payment"; keyword-seeded normal dialogues produced the most false positives. The UNC (uncertain) class trades recall and timeliness for precision. — [arXiv 2502.03964](https://arxiv.org/html/2502.03964v1)
- Metadata FPs: T-Mobile users "report false positives that caused them to miss legitimate calls"; app judged unintuitive. — [SlashGear](https://www.slashgear.com/2200747/tmobile-report-spam-feature-effectiveness/); AT&T uses human review precisely to avoid suspending school-district style callers. — [AT&T](https://www.att.com/es-us/sdabout/pages/cyberaware/ni/robocall)
- Apple Call Screening: users report missing important calls and want clearer indication that screening is active. — [TechRadar](https://www.techradar.com/phones/iphone/call-screening-in-ios-26-has-finally-ended-my-spam-call-nightmare-heres-how-to-set-it-up)
- Google's mitigations: off by default/opt-in; on-device only; no audio or transcript stored or transmitted; beep at call start and every few minutes "so participants know the feature is on"; per-call disable; "Not a scam" button; explicit disclaimer that it "isn't 100% accurate." — [Google support](https://support.google.com/phoneapp/answer/15654065?hl=en)
- Safety-filter refusals as a failure mode: multimodal LLMs declined to process intimidating/profane scam audio, which were counted as false negatives. — [arXiv 2606.24523](https://arxiv.org/pdf/2606.24523)
- Consent law (2025): all-party consent states are California, Connecticut, Delaware, Florida, Illinois, Maryland, Massachusetts, Michigan (unsettled), Montana, Nevada, New Hampshire, Pennsylvania, Washington. Federal ECPA/Wiretap Act is one-party. "The same consent obligations apply whether a person or an AI tool captures a conversation." Recommended practices: announce at start, use consent prompts, restrict transcript access, treat voice/transcripts as personal data; Illinois BIPA is a concern if voiceprints are created. The article does not address whether unstored real-time transcription is "recording." — [Reed Smith](https://www.reedsmith.com/our-insights/blogs/employment-law-watch/102ls2n/the-legality-of-ai-powered-recording-and-transcription/)
- Operational constraint from Google: SIM must be associated with a supported country and the phone must physically be in it; feature gated by region. — [Google support](https://support.google.com/phoneapp/answer/15654065?hl=en)

### Inferences
- A cloud-transcription prototype (e.g., streaming audio to ElevenLabs and an LLM) is legally more exposed than Google's on-device design, especially in MA/CA/FL/IL. For a demo, the safe pattern is: only the user's own device audio with an explicit on-screen notice, a periodic audible tone, no persistence, and a disclaimer; or demo on simulated/consented calls.
- Alert design should expose uncertainty (three-tier: watching / caution / likely scam) rather than a binary "scam" popup, matching both the UNC-prompt finding and RealCall's "uncertain" output.
- Capturing "Not a scam" feedback is the only in-product precision signal any shipping system has; a prototype can log it to tune thresholds.

### Gaps
- No court decision or regulator guidance found on whether ephemeral, unstored AI transcription of a call constitutes interception under state wiretap laws.
- No published alert-fatigue or trust study for in-call scam warnings.

## Q6. What does ElevenLabs offer for streaming STT (Scribe) and AI speech detection usable in a prototype?

### Takeaway
ElevenLabs Scribe v2 Realtime is a production WebSocket STT (`scribe_v2_realtime`, ~150 ms, 90+ languages, PCM 8-48 kHz or mu-law, partial and committed transcripts, VAD or manual commit, $0.28/hour) that fits a live-call pipeline; its AI speech detector is UI-only and limited to ElevenLabs-generated audio, so it is not a general deepfake API.

### Cited Findings
- Endpoint `wss://api.elevenlabs.io/v1/speech-to-text/realtime?model_id=scribe_v2_realtime`; auth via `xi-api-key` header server-side or single-use token client-side. Example input: 16 kHz mono 16-bit PCM in 32,000-byte (1 s) chunks. Server events: `session_started`, `partial_transcript`, `committed_transcript`, `committed_transcript_with_timestamps`, `input_error`; client sends `input_audio_chunk` with `audio_base_64`, `commit`, `sample_rate`. Python (`elevenlabs.speech_to_text.realtime.connect`) and TypeScript SDKs plus raw WebSocket examples. — [ElevenLabs docs: server-side streaming](https://elevenlabs.io/docs/eleven-api/guides/how-to/speech-to-text/realtime/server-side-streaming.md)
- Product page: streaming transcription "in about 150 ms" (another section says under 100 ms), 90+ languages, VAD-based segmentation, manual commit control, PCM 8-48 kHz and mu-law, predictive transcription, text conditioning across reconnects, WebSocket or REST; pricing "$0.28 per hour & lower on annual Business plans"; no numeric WER published, only a comparison chart vs Gemini Flash 2.5, GPT-4o Mini, Deepgram Nova 3. Diarization and dual-channel are listed as FAQ headings without answers. — [ElevenLabs Realtime STT](https://elevenlabs.io/realtime-speech-to-text)
- Scribe v2 Realtime launch covered Nov 2025 as "sub-150 ms" across 90+ languages. — [CXO Digital Pulse](https://www.cxodigitalpulse.com/elevenlabs-launches-scribe-v2-realtime-for-sub-150-ms-live-transcription-across-90-languages/)
- AI speech detection: Audio Detector (watermark) + legacy AI Speech Classifier (99% precision / 80% recall on unmodified ElevenLabs audio); ElevenLabs-only; UI access (classifier page needs no login; Audio Detector needs login); no API documented; prone to false positives on modified audio. — [ElevenLabs docs](https://elevenlabs.io/docs/eleven-creative/audio-tools/audio-detector)
- Independent evidence Scribe is adequate for this task: Turkish scam study used Scribe V1 transcripts and found uncorrected ASR cost only ~0.008 F1 vs human-corrected. — [arXiv 2606.24523](https://arxiv.org/pdf/2606.24523)

### Inferences
- A viable hackathon architecture: mic/VoIP audio (mu-law 8 kHz is accepted, so Twilio media streams can be piped directly) -> Scribe v2 Realtime WebSocket -> on each `committed_transcript`, append to a rolling window -> LLM scoring with an explicit criteria rubric and FRAUD/UNCERTAIN/SAFE output -> hysteresis over several turns -> tiered on-screen alert with "Not a scam" feedback. Latency budget: ~150 ms ASR plus one LLM call per turn.
- Because the 8 kHz mu-law path is supported, the same pipeline can run on a server-side SIP/Twilio call, where STIR/SHAKEN headers are also readable, giving a metadata plus content fusion that no consumer app currently demonstrates.
- Speaker separation matters for scam detection (the scammer's utterances carry the signal); Scribe's diarization status in realtime is unconfirmed, so a prototype should use dual-channel telephony audio (separate inbound/outbound streams) rather than rely on diarization.

### Gaps
- Supported-language list and free-tier/concurrency limits for Scribe v2 Realtime not stated on the fetched pages.
- Whether realtime Scribe supports speaker diarization or dual-channel natively is unanswered in ElevenLabs' own FAQ.
- No general-purpose (any-vendor) voice deepfake API from ElevenLabs.

## Where a hackathon prototype could credibly claim new ground (synthesis)

### Takeaway
The unclaimed space is a transparent, metric-reporting, multi-signal fusion that no shipping product or paper demonstrates end to end: live transcript intent scoring with an explicit rubric and uncertainty tier, fused with call metadata (unknown number, claimed institution vs actual number, attestation when available), evaluated on English hard negatives with measured utterance-to-alert latency.

### Cited Findings
- No shipping product publishes precision/recall or time-to-alert (Google: "isn't 100% accurate" only — [Google support](https://support.google.com/phoneapp/answer/15654065?hl=en); Pindrop/Reality Defender/Truecaller: no metrics — [Pindrop](https://pindrop.com/products/liveness-detection), [RealCall](https://www.realitydefender.com/product/realcall), [Help Net Security](https://www.helpnetsecurity.com/2024/05/29/truecaller-ai-call-scanner/)).
- Academic work is post-hoc and non-English: Korean benchmark "does not test real-time detection or continuous monitoring" — [LREC 2026](https://aclanthology.org/2026.lrec-1.585.pdf); Korean SLM paper does not evaluate partial/streaming detection — [arXiv 2506.06180](https://arxiv.org/html/2506.06180v1); Chinese real-time paper reports no latency and no user study — [arXiv 2502.03964](https://arxiv.org/html/2502.03964v1).
- Precision on hard negatives is the known weak point (0.70-0.77 real-time) and explicit criteria plus an uncertain class are the known fixes — [arXiv 2502.03964](https://arxiv.org/html/2502.03964v1), [arXiv 2506.06180](https://arxiv.org/html/2506.06180v1).
- Earlier detection via message-level sensitive-request detector plus retrieval of similar snippets (F1 0.74 at five messages) — [arXiv 2406.12263](https://arxiv.org/html/2406.12263v2).

### Inferences
- Claimable differentiators: (1) explainable alerts that cite the specific rubric items triggered (impersonation, urgency, payment-rail request, secrecy) instead of a bare "suspicious activity" banner; (2) a visible confidence meter with FRAUD/UNCERTAIN/SAFE states and hysteresis; (3) explicit mismatch detection between claimed identity in the transcript ("this is Chase fraud department") and metadata (number not in contacts, not Chase's published number, attestation B/C); (4) measured and displayed latency and a small English hard-negative test set (bank fraud-department call, airline rebooking, pharmacy verification) with reported precision/recall; (5) a consent-first UX borrowing Google's beep and per-call off switch.
- Avoid over-claiming on voice deepfake detection; no open, validated general detector exists in the sources, and ElevenLabs' classifier is vendor-specific.

### Gaps
- No English real-call public dataset was found; a prototype would need to synthesize or script test calls and should say so.
- The RAG-based real-time fraud detection paper (arXiv 2501.15290) was not read and may overlap with the retrieval idea.
