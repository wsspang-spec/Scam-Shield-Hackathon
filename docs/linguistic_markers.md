# Linguistic, Conversational and Psychological Markers of Scam Calls (Vishing) vs. Legitimate Calls

Scope note: English-language, US-centric phone scams, drawing on academic security/psychology literature (2009-2026) plus US regulator guidance (FTC, FBI/IC3, IRS, SSA OIG, CFPB) and bank fraud-awareness pages. Evidence strength is tagged per finding: **[Strong]** = peer-reviewed empirical work with data; **[Moderate]** = peer-reviewed theory/taxonomy or large regulator corpus; **[Guidance]** = official consumer guidance (authoritative on what legit orgs do, but not quantified); **[Weak]** = industry blog/single-source anecdote.

---

## Key Question 1: Which persuasion/influence principles appear in scam calls, and what phrases signal each?

### Takeaway
Across the empirical vishing literature, **authority** (claiming to be from a reputable institution) is near-universal (95% of 86 real vishing cases), followed by **social proof**, **distraction/fear**, and **liking/helpfulness**; explicit commitment/reciprocity tactics are rare (26%). Time pressure is applied to the *information or problem* ("this is time-sensitive") more than to the caller ("I'm in a hurry"). Stajano & Wilson's seven principles (distraction, social compliance, herd, dishonesty, kindness, need & greed, time) remain the foundational taxonomy and map directly onto detectable phrases.

### Cited Findings

**Foundational taxonomy (Stajano & Wilson 2011, Cambridge)** [Moderate]
- Seven principles: Distraction, Social Compliance (authority), Herd, Dishonesty, Kindness, Need & Greed, Time. — [Stajano & Wilson 2011](https://www.cl.cam.ac.uk/~fms27/papers/2011-StajanoWil-scam.pdf)
- Distraction: "While we are distracted by what grabs our interest, hustlers can do anything to us and we won't notice." In 419 scams, repeated "unexpected" fees keep the mark fixed on the promised sum. — [Stajano & Wilson 2011](https://www.cl.cam.ac.uk/~fms27/papers/2011-StajanoWil-scam.pdf)
- Social compliance: people are trained to defer to authority; hustlers exploit this "suspension of suspiciousness" (fake policeman, Mitnick posing as police, phishing exploiting trust in banks). — [Stajano & Wilson 2011](https://www.cl.cam.ac.uk/~fms27/papers/2011-StajanoWil-scam.pdf)
- Dishonesty: "Our own inner larceny is what hooks us initially"; victims who helped move money fear prosecution and hide the fraud. — [Stajano & Wilson 2011](https://www.cl.cam.ac.uk/~fms27/papers/2011-StajanoWil-scam.pdf)
- Kindness: "People are fundamentally nice and willing to help. Hustlers shamelessly take advantage of it." — [Stajano & Wilson 2011](https://www.cl.cam.ac.uk/~fms27/papers/2011-StajanoWil-scam.pdf)
- Need & Greed: "If we want to con someone, all we need to know is what they want, even if it doesn't exist"; 419 targets are often "not greedy, just depressed and hopeful." — [Stajano & Wilson 2011](https://www.cl.cam.ac.uk/~fms27/papers/2011-StajanoWil-scam.pdf)
- Time: "When under time pressure to make an important choice, we use a different decision strategy." Example phishing phrase: "You'll lose access to your bank account if you don't confirm your credentials immediately." — [Stajano & Wilson 2011](https://www.cl.cam.ac.uk/~fms27/papers/2011-StajanoWil-scam.pdf)

**Empirical frequency in real vishing (Jones, Armstrong, Tornblad & Namin 2020, *Information & Computer Security*)** [Strong]
- Coded 86 real-world vishing cases (from 68 articles/videos) against Ferreira et al.'s (2015) five merged "principles of persuasion in social engineering" (PPSE), which integrate Cialdini, Gragg, Stajano-Wilson and Mouton. Frequencies: Authority 95.3%; Social proof 90.7%; Distraction 89.5%; Liking/similarity/deception 75.6%; Commitment/reciprocation/consistency 25.6%. — [Jones et al. 2020](https://par.nsf.gov/servlets/purl/10281805)
- Most common combination (48.2% of attacks): authority + distraction + liking/deception + social proof. — [Jones et al. 2020](https://par.nsf.gov/servlets/purl/10281805)
- Most consistent implementation elements: "claiming to be from a reputable institution" and "stressing the benefits of complying." Claiming direct authority over the victim and explicitly saying the caller is in a hurry were *rare*; instead callers claimed authority to access the requested information and said *the information itself* was time-sensitive. — [Jones et al. 2020](https://par.nsf.gov/servlets/purl/10281805)
- Flattery/flirting and commitment ladders were uncommon because they seem out of place on an unsolicited call. Attacker initiated 71% of calls; goal was money 51%, information 45%. Coder reliability G = 0.64. — [Jones et al. 2020](https://par.nsf.gov/servlets/purl/10281805)
- Ferreira, Coventry & Lenzini (2015) is the source of the five-principle merged taxonomy; they found principles appear in "specific combinations" in phishing. — [Ferreira et al. 2015](https://irisc-lab.uni.lu/principles-of-persuasion-in-social-engineering-and-their-use-in-phishing/)

**Empirical frequency in scam-baiter call corpus (Wood, Kepkowski, Zinatullin, Darnley & Kaafar 2023, Macquarie Univ.)** [Strong]
- 341 transcripts (~90 hours, 15,234 scammer utterances) of SSN, refund, tech-support and reward scams. Social-engineering techniques observed with example phrasing:
  - Authority: "My name is officer Carol Snyder."
  - Distraction and fear: "This is suspicious activity on the Amazon account..."
  - Intimidation / non-interruption: "Do not interrupt me in between."
  - Threats: "I'm sending the cops to your house."
  - Reciprocation / helper framing: "There is no need to worry because I'm here to help you."
  - Commitment: asking whether the victim wants to fix the problem / receive the gift, then building on the "yes."
  - Liking/rapport: chit-chat deliberately placed near payment requests.
  - Social proof: the authors found *little evidence* of this technique (contrasts with Jones et al.). — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- Emotion model (RoBERTa, Ekman): surprise and anger were the most common scammer emotions across scam types. — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)

**Controlled experiment on authority/fear/reward (Tu, Doupe et al., USENIX Security 2019)** [Strong]
- 3,000 ASU staff phones, 10 experiments. 4.93% pressed at least one SSN digit (3.70% "possibly tricked" after filtering). — [Tu et al. 2019](https://www.usenix.org/system/files/sec19-tu.pdf)
- Entity impersonated (internal HR vs IRS) was the most significant factor (d = 0.331); 202 area code vs 800 was marginally significant (d = 0.222). **Fear vs. reward framing was NOT significant**, nor were accent, human vs. synthetic voice, or caller name. Best condition (spoofed internal HR name) reached 10.33%; worst (IRS unclaimed refund) 0.33%. — [Tu et al. 2019](https://www.usenix.org/system/files/sec19-tu.pdf)
- Script phrasing used: "This is an urgent notice! This is a final notice from the IRS." / "Your action is required immediately, or a penalty will be assessed." / refund "due to expire within three days." — [Tu et al. 2019](https://www.usenix.org/system/files/sec19-tu.pdf)

**Psychology of susceptibility** [Moderate]
- Modic (2012 PhD, Exeter): self-control was the strongest predictor of scam compliance; authority compliance and social influence strongly predicted *responding* in study 2; need for consistency strongly predicted responding in both studies; "negative urgency" (impulsivity) influenced response rates. — [Modic 2012](https://ore.exeter.ac.uk/repository/handle/10871/8044?show=full)
- Langenderfer & Shimp (2001) visceral-influence theory: strong visceral states (greed, fear, lust) cause targets to "set aside the message's rational elements and focus on the desired outcome," reducing scrutiny of fraud cues. — [Stanford Center on Longevity summary](https://longevity.stanford.edu/consumer-vulnerability-to-scams-swindles-and-fraud-a-new-theory-of-visceral-influences-on-persuasion)

**Regulator-documented phrasing by principle** [Guidance]
- FTC four signs: (1) impersonation of a known org; (2) a problem or a prize ("you owe money," "legal trouble," "family emergency," "computer virus," "won a lottery but must pay a fee"); (3) pressure to act immediately, "may tell you not to hang up," threats of arrest, lawsuit, license loss, deportation; (4) demand for a specific payment method. — [FTC How to Avoid a Scam](https://consumer.ftc.gov/system/files/consumer_ftc_gov/pdf/How-to-avoid-a-scam_English_August2023.pdf)
- Authority props: fake name + badge number, "auditor," caller ID showing "Internal Revenue Service" or the IRS's real number; voicemail giving "24 hours to return the call." — [CFPB IRS imposter blog](https://www.consumerfinance.gov/about-us/blog/tax-season-protect-yourself-irs-imposter-scams/)
- Fear/authority (law-enforcement impersonation): missed jury duty / court date with "a warrant for the victim's arrest"; expiring passport/license requiring a "renewal fee"; threats to revoke medical licenses; extradition threats; "urgent, aggressive tones." — [FBI IC3 PSA Sept 2026](https://www.ic3.gov/PSA/2026/PSA260917)
- Escalating aggression when questioned; inflated "fees or court costs in the thousands"; "settlement" payments. — [FBI Detroit](https://www.fbi.gov/contact-us/field-offices/detroit/news/press-releases/fbi-detroit-warns-public-to-beware-of-government-impersonation-scams)
- Safety/protection framing (authority + fear + helper): "temporary safe account," "federal protection," "segregated holding account," "move your money immediately." — [Hacked.com / FTC summary](https://hacked.com/move-your-money-to-protect-it-scam/)
- Bank-impersonation urgency + helper: "We want to stop the charge before it goes through"; "Just read the code back to me and we'll lock the account." — [Texas Regional Bank](https://trb.bank/all/bank-fraud-department-impersonation-scam/)
- "I just need to verify your identity." / "Please read it back to me so I can cancel the transaction." / "calm, reassuring tone to build trust while creating urgency." — [First Mid Bank](https://www.firstmid.com/articles/your-bank-will-never-ask-you-this)
- Generic account lures: "update your account," "validate your login," paired with urgent or coercive language. — [Security Boulevard](https://securityboulevard.com/2025/06/using-ai-to-identify-patterns-in-vishing-attempts/) [Weak]
- SMS analogue (UK 7726 corpus, 213,659 scam texts): Authority lure present in 67% of government, 47% telecom, 44% banking, 38% delivery scams; Need & Greed 12-14%; Time/Urgency in all types; Herd and Dishonesty not observed. — [7726 SMS study 2025](https://arxiv.org/pdf/2508.05276)

### Inferences
- For a rubric, weight **authority claim + unsolicited contact + sensitive request** as the core triad; it covers ~95% of documented vishing. Social proof and herd are weak/inconsistent signals on phone (Jones found 91% but Wood found little; 7726 found none), so do not rely on them.
- Urgency in scams is typically **object-directed** ("the account will be locked," "warrant will be issued," "refund expires in 3 days") rather than caller-directed ("I'm busy"). Caller-directed hurry is more typical of legitimate busy agents.
- Fear and reward framings are equally effective (Tu et al.), so a rubric should treat "prize" and "problem" hooks symmetrically.
- Fake authority props (badge number, case ID, officer name, "auditor") are cheap for scammers and rare in legit first-contact calls, making them a high-value lexical feature.

### Gaps
- No study provides a frequency table of *specific phrases* across a large US English voice corpus; phrase examples come from small qualitative samples (Wood et al. 341 transcripts, Tabron ~handful of IRS calls) or guidance pages.
- Could not access the full Ferreira et al. (2015) text for their per-principle phishing frequencies (only abstract).
- Modic/Lea quantitative effect sizes not available from the abstract.

---

## Key Question 2: What structural stages of a scam call does academic work identify?

### Takeaway
Multiple independent lines of work converge on a four-stage arc: (1) credible introduction/authority hook, (2) problem explanation that creates fear or hope, (3) "helpful" step-by-step instructions that build compliance (often remote access or form-filling), (4) financial/data extraction, sometimes followed by a disorganised close with a promised callback. Multi-handoff "transfer" structures (tech support -> bank -> government) and supervisor escalation are documented add-ons.

### Cited Findings

**HMM-derived stage structure (Wood et al. 2023)** [Strong]
- Shared high-level structure across SSN, refund, support, reward scams: (1) Greetings (character-specific self-introduction, e.g., "Hello. And thank you for calling..."); (2) Problem explanation (compromised account, fraudulent order, criminal investigation tied to identity); (3) Instructions (install remote-access software, fill forms, visit websites); (4) Financial exploitation (payment, gift cards, bank details, transfers). — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- SSN-scam sub-stages included: detailed call-reason description, asking about identity theft, chit chat, gift card payment, **redirection to supervisor**, ID and PII requests, case and procedure explanation, **providing case ID**. — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- Refund-scam sub-stages: web browser instructions, device check, download/installation instructions, cancellation and refund options, payment instructions, bank account and refund steps. — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- Stage-prediction accuracy of the HMM (relaxed/strict): SSN 0.81/0.54; refund 0.83/0.59; support 0.70/0.47; reward 0.91/0.50. Scam *type* classification with RoBERTa: F1 85-95% from one utterance, 92-98% from 5-6 utterances. — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- Press summary of the same study framed stages as Introduction (credible, authoritative, calm description of a serious threat attributed to a higher authority) -> Assistance (helpful guide, rapport, step-by-step) -> Threat (emotions escalate; police, court orders, arrest warrants, jail; legal-sounding terms; **talk over the victim to avoid questions**; time pressure) -> Payment/Close (conversation becomes less organised, call ends, sometimes promising a callback to confirm). Model "looks for particular phrases and keywords, and common transitions between topics." — [Macquarie Lighthouse 2022](https://lighthouse.mq.edu.au/article/may-2022/Tricks-used-by-phone-scammers-exposed-in-new-study)

**Tech-support scam call structure (Miramirkhani, Starov & Nikiforakis, NDSS 2017)** [Strong]
- 60 recorded calls (22+ hours). Stages: Contact (scammer takes control) -> Remote access (LogMeIn Rescue 60%, GoToAssist 21%, TeamViewer 12%) -> Fake diagnosis -> Pricing (2-3 packages, middle framed as best value, $69.99-$999.99, mean $290.90) -> Exit. — [Miramirkhani et al. 2017](https://arxiv.org/pdf/1607.06891.pdf)
- Fake-diagnosis techniques by share of calls: stopped services/drivers 67% ("hackers stopped these"); Event Viewer errors 52%; named malware ("koobface," "Zeus") 50%; System Information 47%; Action Center 40%; fake command-line scan showing "Virus detected"/"System at Risk" 40%; netstat as "attackers connected" 40%. — [Miramirkhani et al. 2017](https://arxiv.org/pdf/1607.06891.pdf)
- Mean time from call start to pricing ~17 min; authors suggest calls >41 min likely indicate a defrauded victim. Scammers spoke ~1,367 +/- 407 words per call vs ~530 +/- 172 for the researcher (scammer dominates talk time). Background call-center voices audible on 62% of calls. — [Miramirkhani et al. 2017](https://arxiv.org/pdf/1607.06891.pdf)
- Manner was "patient, kind," step-by-step, sometimes opening Wikipedia to explain terms; when challenged, 60% stayed calm and offered websites as proof, 40% became rude. — [Miramirkhani et al. 2017](https://arxiv.org/pdf/1607.06891.pdf)

**Multi-phase handoff structures** [Guidance]
- FBI "Phantom Hacker" (IC3): Phase 1 tech-support impersonation (pop-up/call, PC scan "reveals" problem, remote access, watch victim log into bank, "a bank employee will call soon"); Phase 2 bank impersonation ("a hacker has compromised your accounts," move funds to "supposedly safe third-party account" controlled by a "trustworthy US government agency," via wire/cash/crypto, repeated over days or months); Phase 3 government impersonation (Federal Reserve, fake letterhead, funds "unsafe unless moved to an account under their protection"). Victims told "not to inform anybody of the real reason why they are moving their funds." Seniors lost $4.885B in 2024 (+43% YoY), average loss $83,000. — [Fortra summary of FBI PSA](https://www.fortra.com/blog/fbi-warns-seniors-targeted-three-phase-phantom-hacker-scams)
- SSA OIG fake-transfer scam: retailer/bank/police caller raises a suspicious purchase; when denied, "transfers" victim to "Social Security" or "OIG," who says the SSN was stolen/used in crimes and pressures to sign documents, stay silent, grant device access, pay for a new number, or move money. "Legitimate companies and other agencies CANNOT transfer your phone call directly to SSA or OIG... it is a scam, without exception, every time." — [SSA OIG July 2026](https://oig.ssa.gov/assets/uploads/2026-july-fake-call-transfers.pdf)
- Grandparent scam structure: (1) unexpected dire emergency ("Your grandson has been arrested and needs bail money"; "Your granddaughter was at fault in a car crash..."); (2) immediate payment demand; (3) secrecy request, sometimes justified by a judge's "gag order"; (4) escalation with further secret payments. Impersonated roles: grandchild, police officer, lawyer. — [National Cybersecurity Alliance](https://staysafeonline.org/articles/when-scammers-call-grandma)
- Amazon refund scam: "fraud on your account, you're owed a refund" -> remote access -> log into Amazon then bank "so the refund could be processed" -> "refunded too much" -> repay overage in gift cards. — [Geebo](https://blog.geebo.com/2021/04/07/amazon-refund-call-is-a-scam/) [Weak]

### Inferences
- A transcript-level rubric should score **stage progression**, not just presence of keywords: an authority intro followed within a few turns by a problem statement, then instructions, then a payment/PII request is the canonical signature. Legitimate calls rarely traverse all four.
- **Talk-time asymmetry** (scammer ~2.5x the victim's word count in Miramirkhani) and **scammer-initiated topic transitions** are measurable structural features.
- **Intra-call transfers** to a second, more authoritative persona ("let me connect you to my supervisor / the Federal Reserve / SSA") are a strong scam marker; SSA OIG states it is a scam "every time."
- A disorganised or abrupt close after payment, with a promised confirmation callback, is a late-stage tell but less useful for real-time detection.

### Gaps
- Wood et al.'s data are scam-baiter calls, not real victims, so stage timing may differ from genuine calls.
- No academic source quantifies stage structure for grandparent/family-emergency or romance/pig-butchering voice calls (those were "marginal" in Wood et al. and excluded).

---

## Key Question 3: Which conversational-dynamics features matter (scripting, control, secrecy, isolation, channel moves, elicitation, payment tells)?

### Takeaway
The highest-confidence transcript-detectable behaviours are: refusal to allow hang-up/callback, instructions to stay on the line and not tell anyone (family, bank, police), requests to read back OTPs or give PIN/SSN/card data under the guise of "verification," transfer to a second persona, remote-access instructions, and demands for gift cards, crypto, wire, cash courier or moving money to a "safe account." Conversational-control markers (interruption, deferring the victim's questions, answering questions with questions, polar tag questions "OK?/All right?") are documented qualitatively in forensic-linguistic work.

### Cited Findings

**Conversational control and discourse (Tabron, Black Hat USA 2016, forensic linguistics of IRS scam calls)** [Moderate; small sample, no legit baseline]
- Interruption / topic control: caller's "Can I just --" met with a flat "No." — [Tabron 2016](https://www.blackhat.com/docs/us-16/materials/us-16-Tabron-Language-Properties-Of-Phone-Scammers-Cyberdefense-At-The-Level-Of-The-Human.pdf)
- Question deferral: scammers push off informational questions (addresses, where to mail, which store) to "later"; some questions ignored entirely ("What's your name?"). — [Tabron 2016](https://www.blackhat.com/docs/us-16/materials/us-16-Tabron-Language-Properties-Of-Phone-Scammers-Cyberdefense-At-The-Level-Of-The-Human.pdf)
- Responding to a question with a question (e.g., to "Are you ready?"). — [Tabron 2016](https://www.blackhat.com/docs/us-16/materials/us-16-Tabron-Language-Properties-Of-Phone-Scammers-Cyberdefense-At-The-Level-Of-The-Human.pdf)
- Polar tag questions ("OK?", "All right?") used 7-33 times per sample to elicit agreement accepting terms just stated. — [Tabron 2016](https://www.blackhat.com/docs/us-16/materials/us-16-Tabron-Language-Properties-Of-Phone-Scammers-Cyberdefense-At-The-Level-Of-The-Human.pdf)
- Speech acts dominated by **directives** (withdraw cash, go to bank/store, buy payment vouchers) and **threat assertions** (police coming to arrest). — [Tabron 2016](https://www.blackhat.com/docs/us-16/materials/us-16-Tabron-Language-Properties-Of-Phone-Scammers-Cyberdefense-At-The-Level-Of-The-Human.pdf)
- Narrative-structure violations (Labov): scammer accounts lack orientation, evaluation and resolution; complicating action without resolution. Honorific "ma'am" and markers "OK"/"All right" frequent; repetition of "are you ready?" — [Tabron 2016](https://www.blackhat.com/docs/us-16/materials/us-16-Tabron-Language-Properties-Of-Phone-Scammers-Cyberdefense-At-The-Level-Of-The-Human.pdf)
- Wood et al. corroborate non-interruption demands: "Do not interrupt me in between." and "talk over the victim to avoid questions." — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965); [Macquarie Lighthouse](https://lighthouse.mq.edu.au/article/may-2022/Tricks-used-by-phone-scammers-exposed-in-new-study)

**Stay-on-the-line / don't hang up** [Guidance, multiple independent authorities]
- FTC: scammers "may tell you not to hang up." — [FTC](https://consumer.ftc.gov/system/files/consumer_ftc_gov/pdf/How-to-avoid-a-scam_English_August2023.pdf)
- FBI IC3: "keeping victims on the phone for the duration of the scam" and "refusing to speak to or leave messages with anyone other than the targeted victim." — [IC3 PSA 2026](https://www.ic3.gov/PSA/2026/PSA260917)
- Bank: "Telling you not to hang up or call anyone else." — [First Mid Bank](https://www.firstmid.com/articles/your-bank-will-never-ask-you-this)
- "Move your money" scam: caller "may stay on the line while the victim goes to the bank and coaches them on what to say." — [Hacked.com](https://hacked.com/move-your-money-to-protect-it-scam/)

**Secrecy and isolation** [Guidance, multiple authorities]
- FBI IC3: "urging victims not to tell family, friends, financial institutions, or law enforcement about the call." — [IC3 PSA 2026](https://www.ic3.gov/PSA/2026/PSA260917)
- SSA OIG: "SSA or OIG will never ask you to keep the call a secret!" Listed warning sign: "Requests for secrecy." — [SSA OIG 2026](https://oig.ssa.gov/assets/uploads/2026-july-fake-call-transfers.pdf)
- Phantom Hacker: victims told "not to inform anybody of the real reason why they are moving their funds." — [Fortra/FBI](https://www.fortra.com/blog/fbi-warns-seniors-targeted-three-phase-phantom-hacker-scams)
- Grandparent scam: tell no one including family; "gag order" justification. — [NCA](https://staysafeonline.org/articles/when-scammers-call-grandma)
- Legit fraud teams "do not need the victim to hide the transfer's purpose from their own bank." — [Hacked.com](https://hacked.com/move-your-money-to-protect-it-scam/)

**Information elicitation ("verify" inversion)** [Guidance + Strong empirical]
- OTP read-back: "Just read the code back to me and we'll lock the account"; requests for debit card digits and SSN "to verify a few details." — [TRB](https://trb.bank/all/bank-fraud-department-impersonation-scam/)
- CIBC: caller asks you to read back the 6-digit one-time verification code "as a way to secure your account" or as part of "account recovery." — [CIBC](https://www.cibc.com/en/privacy-security/banking-fraud/frauds-and-scams/bank-impersonator-scams.html)
- Legit fraud calls verify "using information it already has, rather than asking you for information." — [First Mid Bank](https://www.firstmid.com/articles/your-bank-will-never-ask-you-this)
- In the Tu et al. experiment the extraction target was the last 4 SSN digits after a fake "connecting you to a live agent" message that "lends legitimacy before the SSN request." — [Tu et al. 2019](https://www.usenix.org/system/files/sec19-tu.pdf)
- Real-time LLM study: suspicious keywords carried from prior work include "payment" and "ID"; scam flagged after "personal information" and "credit card fraud"; request for ID-card information was the decisive turn. — [Shen et al. CHI 2025 LBW](https://arxiv.org/html/2502.03964v1)

**Remote access / device control** [Strong + Guidance]
- Remote-admin tool installation and session code sharing is stage 2 of every tech-support scam call (60/60). — [Miramirkhani et al. 2017](https://arxiv.org/pdf/1607.06891.pdf)
- Wood et al. "Instructions" stage: install remote-access software, fill forms, visit websites. — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- "No legitimate company needs remote access to your computer." — [Geebo](https://blog.geebo.com/2021/04/07/amazon-refund-call-is-a-scam/) [Weak]
- SSA OIG lists "grant device access" among scam pressures. — [SSA OIG 2026](https://oig.ssa.gov/assets/uploads/2026-july-fake-call-transfers.pdf)

**Channel moves and handoffs** [Guidance + Moderate]
- Intra-call "transfer" to SSA/OIG is "a scam, without exception, every time." — [SSA OIG 2026](https://oig.ssa.gov/assets/uploads/2026-july-fake-call-transfers.pdf)
- "Redirection to supervisor" is a recurring SSN-scam sub-stage. — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- SMS analogue: Wrong Number / Hi Mum-Dad scams aim to move the victim to a new number or WhatsApp; banking "callback" scams cite a fake transaction/OTP and ask the recipient to call a number (described as a rising trend). — [7726 study](https://arxiv.org/pdf/2508.05276)

**Payment-method tells** [Guidance, unanimous across agencies]
- FTC: insist on cryptocurrency, wire service, payment app, or gift cards "including giving them the card numbers"; fake-check-and-send-back variant. "Honest businesses" never require these. — [FTC](https://consumer.ftc.gov/system/files/consumer_ftc_gov/pdf/How-to-avoid-a-scam_English_August2023.pdf)
- IRS will not "demand immediate payment through a specific method, such as a prepaid debit card, gift card, or wire transfer"; checks payable to anyone other than "U.S. Treasury" are a tell. — [IRS](https://www.irs.gov/node/59151)
- FBI IC3 government impersonation: prepaid cards, couriers, bank wires, cryptocurrency, "cash deposited into cryptocurrency kiosks." — [IC3 PSA 2026](https://www.ic3.gov/PSA/2026/PSA260917)
- FBI: will never "ask people to use large sums of their own money to help catch a criminal" or wire a "settlement." — [FBI Detroit](https://www.fbi.gov/contact-us/field-offices/detroit/news/press-releases/fbi-detroit-warns-public-to-beware-of-government-impersonation-scams)
- "Move money to protect it": wire, crypto ATMs, cash or gold to a courier, gift cards, liquidating retirement/brokerage/home-equity, cashier's checks. — [Hacked.com](https://hacked.com/move-your-money-to-protect-it-scam/)
- Grandparent scams: wire, crypto, gift cards, mailed payments, cash via courier. — [NCA](https://staysafeonline.org/articles/when-scammers-call-grandma)
- Scam-baiter corpus: "gift card payment," "payment (gift/debit card)," "fee and gift card instructions" are named HMM stages in SSN, support and reward scams. — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)

**Scripted rigidity / lexical fragility** [Strong, indirect]
- TF-IDF classifiers hit 95-99.6% F1 on the Korean KorCCViD corpus, but LLM-rephrasing that made scammer lines "casual" and added benign filler cut accuracy by up to 30.96% (GPT-4o rewrites: 97.66% -> 81.35% average), showing that classifiers were keying on scripted token patterns. — [Li et al. 2025](https://arxiv.org/pdf/2507.16291)
- Shen et al. (2024): Random Forest scored F1 1.00 on public datasets but 0.26 on synthetic data built to share the same top-50 TF-IDF terms across scam and legit, meaning high keyword scores "came from specific terms common in fraudulent conversations, which scammers could avoid." — [Shen et al. 2024](https://arxiv.org/html/2409.11643v2)

### Inferences
- **Direction of information flow** is the single cleanest discriminator: scammers ask the callee to *supply* identifiers/codes; legitimate fraud departments *confirm* using data they already hold and ask yes/no about transactions.
- **Control markers** (don't hang up, don't call anyone, don't interrupt, stay on the line, I'll stay with you while you go to the store/bank) are near-exclusive to scams; no regulator or bank describes a legitimate reason for them.
- Rubric should treat **any payment instruction naming gift cards, crypto kiosk, wire to a new account, cash courier, or "safe/segregated/protection account"** as near-dispositive given unanimous agency guidance.
- Pure keyword scoring is brittle (Li et al.; Shen et al.); an LLM rubric should score *speech acts and structure* (directive to purchase, request to read back code, instruction to conceal) rather than tokens.

### Gaps
- No quantitative frequency of secrecy or stay-on-line instructions across a voice corpus; evidence is regulator-reported pattern plus qualitative transcripts.
- Tabron's discourse features lack a legitimate-call baseline, so tag-question rates etc. cannot be used as calibrated thresholds.
- No source quantifies "scripted rigidity" directly (e.g., repetition rate or deviation from script when challenged) beyond Miramirkhani's 60/40 calm/rude split when pushed back.

---

## Key Question 4: What are the false-positive traps, and what distinguishes a legitimate verification call?

### Takeaway
Legitimate bank fraud departments, collectors, the IRS, SSA and utilities also use urgency and "verification," so these alone are weak signals. The documented discriminators are: legitimate callers never ask for OTPs/PINs/passwords/full card numbers, verify with information they already hold (yes/no on a transaction), never demand a specific irreversible payment channel, give you the right to question/appeal and time to decide, provide identifying details (name, company, address, license), and invite you to hang up and call back the official number. Real-time LLM detectors show measurable false-positive rates on legitimate calls containing words like "payment" or "ID."

### Cited Findings

**Empirical false-positive evidence** [Strong]
- Shen et al. (CHI 2025 LBW): real-time LLM detection achieved recall 0.98-1.00 but precision only 0.70-0.77 on synthetic normal dialogues that deliberately contained suspicious keywords (vs 0.95-1.00 retrospectively). Example FP: a flight re-booking call flagged at utterance 15 because the agent said "payment." False positives shared "identity verification, financial information sharing, and urgent decision-making" patterns. Adding an UNCERTAIN option raised precision (ERNIE 0.70 -> 0.85) at the cost of recall (0.90-0.98) and delayed warnings. — [Shen et al. 2025](https://arxiv.org/html/2502.03964v1)
- Shen et al. (2024): LLM precision >0.98 on real data but recall as low as 0.72; authors stress balancing recall with precision "to avoid misclassifying genuine conversations." — [Shen et al. 2024](https://arxiv.org/html/2409.11643v2)

**What legitimate banks do / never do** [Guidance]
- Legit fraud call: asks whether you recognize a specific transaction; verifies using information it already has; may lock/restrict the card; "encourages you to hang up and call the number on the back of your card if you're unsure." Never asks for "passwords, PINs, or one-time verification codes." — [First Mid Bank](https://www.firstmid.com/articles/your-bank-will-never-ask-you-this)
- TRB: will never initiate a call to ask for a one-time passcode, CVV, or PIN; never text a link; never ask for username/password/token code. — [TRB](https://trb.bank/all/bank-fraud-department-impersonation-scam/)
- CIBC: "CIBC or a government agency will never contact you to ask for your personal or banking information"; find the callback number "from the back of your card, an official website, or an old statement, not from the caller." — [CIBC](https://www.cibc.com/en/privacy-security/banking-fraud/frauds-and-scams/bank-impersonator-scams.html)
- FTC: "Honest organizations won't call, email, or text to ask for your personal information"; "Honest businesses give you time to decide." — [FTC](https://consumer.ftc.gov/system/files/consumer_ftc_gov/pdf/How-to-avoid-a-scam_English_August2023.pdf)

**IRS / tax** [Guidance]
- IRS generally mails a bill first and makes initial contact by USPS; will call/visit only in specific cases (overdue bill, delinquent return, audit, criminal investigation) and "generally you receive several letters first"; presents official ID and can give a dedicated IRS number to verify; offers several payment options; private collectors only after written notice. Will not demand payment "without giving you a chance to question or appeal," threaten police/immigration arrest, or threaten license/immigration-status revocation. (2018 archived page.) — [IRS](https://www.irs.gov/node/59151)
- IRS will never contact by email/text/social media to request PINs, passwords, or account info; scam tells include hostile tone, yelling/insulting, badge number recitation. — [CFPB](https://www.consumerfinance.gov/about-us/blog/tax-season-protect-yourself-irs-imposter-scams/)

**Debt collection (legit collectors also pressure for payment)** [Guidance]
- Legit collector should provide name, company name, street address, phone number, and professional license number if state requires; must provide debt information at first contact or within five days. Scam signs: threats, calls late at night/at work, refusing to give mailing address/phone, withholding debt details, collecting a debt you don't recognize, claiming they can have you arrested or criminally charged, requesting personal financial information. — [CFPB](https://www.consumerfinance.gov/ask-cfpb/what-is-the-fair-debt-collection-practices-act-en-1699/)

**Government / law enforcement** [Guidance]
- FBI will never call/email/text to demand payment or threaten arrest; never ask to wire a "settlement"; never ask you to use your own money to catch a criminal; never call about "frozen" SSNs or inheritances. — [FBI Detroit](https://www.fbi.gov/contact-us/field-offices/detroit/news/press-releases/fbi-detroit-warns-public-to-beware-of-government-impersonation-scams)
- Law enforcement/government will never "contact the public by phone or text to demand any payment or request personal or sensitive information" nor request prepaid card, crypto, or courier payment. Verify "using official contact information you find yourself, not details the caller provides." — [IC3 PSA 2026](https://www.ic3.gov/PSA/2026/PSA260917)
- SSA/OIG never receive transferred calls and never ask for secrecy. — [SSA OIG 2026](https://oig.ssa.gov/assets/uploads/2026-july-fake-call-transfers.pdf)
- No real FTC employee will tell you to move money to protect it. — [Hacked.com citing FTC Feb 2025 alert](https://hacked.com/move-your-money-to-protect-it-scam/)

**Non-obvious trap: scammers are often calm and patient** [Strong]
- Tech-support scammers were "patient, kind," gave step-by-step instructions, and 60% stayed calm and polite when doubted. — [Miramirkhani et al. 2017](https://arxiv.org/pdf/1607.06891.pdf)
- Bank-impersonators use a "calm, reassuring tone to build trust while creating urgency." — [First Mid Bank](https://www.firstmid.com/articles/your-bank-will-never-ask-you-this)
- Jones et al.: explicit "I'm in a hurry" was rare; the helpfulness/"benefits of complying" frame was consistent. — [Jones et al. 2020](https://par.nsf.gov/servlets/purl/10281805)

### Inferences
- A rubric should **down-weight** tone/urgency/verification words alone and **up-weight** the *combination* of (a) inbound unsolicited call, (b) request that the callee supply secrets or make a payment, (c) resistance to callback/verification, (d) specific irreversible payment channel. Legitimate urgency (e.g., "your card is locked, call us back at the number on your card") lacks (b)-(d).
- Positive legitimacy markers to score as *negative evidence*: caller invites callback to an official/published number; verifies with yes/no questions about transactions; offers written notice, appeal, or time; provides full identifying details voluntarily; declines to accept payment details on the call.
- Hostility and aggression are a *sufficient* but not *necessary* scam marker; absence of aggression must not lower the score.
- Agency guidance pages are largely written about what agencies "never" do; they're authoritative for government and bank calls but say little about legitimate utility, medical, or school calls, so those remain under-specified traps.

### Gaps
- No peer-reviewed corpus directly compares legitimate fraud-department calls with impersonation calls on linguistic features; the discriminators above come from institutional guidance, not measured data.
- Utility shut-off scams and doctor's-office/medical-billing legit calls were not covered by sources found; no authoritative "what a legit utility call sounds like" source was located within the call budget.
- Shen et al.'s datasets are in Chinese; English false-positive rates for real-time LLM detection are not reported in the sources found.

---

## Key Question 5: Quantitative results: which features had highest predictive power, and what precision/recall?

### Takeaway
Published classifiers report very high numbers (F1 0.95-1.00) on small or keyword-separable datasets, but ablation/adversarial work shows those numbers rest on scripted lexical patterns and collapse (down to F1 0.26, or -31 pp accuracy) when scam and legitimate texts share vocabulary. LLM zero-shot detection is robust on recall (0.98-1.00) but weaker on precision (0.70-0.77) in real-time keyword-trap settings. No paper found provides a ranked, named feature-importance list for persuasion cues; the best structural result is Wood et al.'s stage HMM and 92-98% F1 scam-type classification from 5-6 utterances.

### Cited Findings
- **Wood et al. 2023**: RoBERTa scam-type classifier F1 85-95% (1 utterance), 92-98% (5-6 utterances); refund vs support hardest to separate; HMM stage prediction accuracy 0.70-0.91 relaxed; emotion features: surprise and anger dominant; word rate ~2-2.5 wps for both scammer and baiter (not discriminative). — [Wood et al. 2023](https://arxiv.org/pdf/2307.01965)
- **Shen et al. 2024** ("Combating Phone Scams with LLM-based Detection"): five LLMs, single prompt, yes/no + reasoning. Precision >0.98 (real) / >0.95 (synthetic); recall as low as 0.72 (real) / 0.86 (synthetic). Random Forest: F1 1.00 on public SC/SD datasets and on real YouTube transcripts, 0.99 on MASC, but 0.26 (precision 0.62, recall 0.16, accuracy 0.53) on synthetic data where both classes contained the top-50 TF-IDF terms. Authors: high ML scores "came from specific terms common in fraudulent conversations, which scammers could avoid"; LLMs "may not rely on keywords only." — [Shen et al. 2024](https://arxiv.org/html/2409.11643v2)
- **Shen et al. 2025** (CHI LBW real-time): recall 0.98-1.00; synthetic precision 0.70-0.77 real-time vs 0.95-1.00 retrospective; real-data precision 0.94-1.00; synthetic accuracy 0.79-0.96; UNC mode precision up to 0.85 with recall 0.90-0.98. Scam flagged at utterance 6 (RT) vs 10 (UNC). — [Shen et al. 2025](https://arxiv.org/html/2502.03964v1)
- **Li, Manickam, Chong & Karuppayah 2025** (ICDF2C, Korean KorCCViD, 609+609 transcripts): LinearSVC F1 0.996, LogReg 0.992, RF 0.988, GradientBoosting 0.956 on TF-IDF; adversarial LLM rephrasing drops accuracy 3.42% (GPT-4o-mini), 16.16% (GPT-4o), 7.18% (Gemini 2.0), 33.83% (Qwen2.5) on 100 samples; GPT-4o on full set 97.66% -> 81.35%, per-classifier drops 2.88-30.96%; all Wilcoxon p<0.05. Classifiers depend on "token occurrence, token uniqueness, and transcript length." — [Li et al. 2025](https://arxiv.org/pdf/2507.16291)
- **Saradha 2025** (Unitec MSc thesis, Kaggle "Fraud Call Dataset" 5,000 transcripts): zero-shot classification scoring transcripts on four social-engineering attributes (impersonation, urgency, authority, sensitive information; abstract also mentions mimicry) achieved accuracy 0.97-0.98 across dataset sizes 1,000-5,000; one missed fraud had weak SET alignment. Dataset annotation validation not described. — [Saradha 2025](https://www.researchbank.ac.nz/server/api/core/bitstreams/30f64218-7cb7-485a-82cb-7a4347802537/content)
- **Zhi, Tee, Ong & Teoh 2025** (IEEE Access, D-STAR sparse-attention transformer, 400 scam + 400 non-scam transcripts from social media/news/forums, ChatGPT-augmented): accuracy 94%, recall 91.67%, F1 84.98%; attention-highlighted words not reported in accessible text. — [Zhi et al. 2025](https://shdl.mmu.edu.my/14319/)
- **Tu et al. 2019**: entity impersonated was the strongest experimental factor (d = 0.331); area code d = 0.222; fear vs reward, accent, synthetic voice, caller name all non-significant. — [Tu et al. 2019](https://www.usenix.org/system/files/sec19-tu.pdf)
- **Jones et al. 2020**: binomial tests showed authority, social proof and distraction used about equally often and significantly more than liking/deception, which was used more than commitment/reciprocity. — [Jones et al. 2020](https://par.nsf.gov/servlets/purl/10281805)
- **Miramirkhani et al. 2017**: call-duration heuristic (>~41 min = mean + 3 SD suggests defrauded victim); price did not correlate with duration (r = 0.11); scammer word count ~1,367 vs victim ~530. — [Miramirkhani et al. 2017](https://arxiv.org/pdf/1607.06891.pdf)
- **Prasad, Dunlap, Ross & Reaves (SnorCall, NDSS 2023 poster)**: weak-supervision labeling of ~1.3M honeypot robocalls into ~26,800 campaigns using expert-written labeling functions, NER/keyword and callback-number extraction; no precision/recall in the poster text. — [SnorCall poster](https://www.ndss-symposium.org/wp-content/uploads/2023/02/NDSS2023Poster_paper_1049.pdf)
- **7726 SMS study**: lure classifier validated on 384 texts, Cohen's kappa 0.73. — [7726 study](https://arxiv.org/pdf/2508.05276)

### Inferences
- Reported F1 near 1.0 should be treated as dataset artefacts; the adversarial and TF-IDF-controlled experiments are the more honest ceiling (roughly 80% accuracy for keyword models under paraphrase).
- An LLM rubric built on *attribute scores* (impersonation, urgency, authority, sensitive-info request), as in Saradha's zero-shot approach, is the closest published analogue to the user's objective and performed at 0.97-0.98 accuracy on a (likely easy) Kaggle set.
- The real-time precision gap (0.70-0.77) indicates that a rubric used mid-call should defer judgment on "payment"/"ID" mentions until a *request directed at the callee to supply or send* appears, which is what the UNC mode effectively did.

### Gaps
- No paper found reports per-feature importance, SHAP values, or ablations naming which persuasion cue (urgency vs authority vs secrecy vs payment method) carries the most weight; Saradha's thesis may contain this in chapters 4-5 but those sections were beyond the fetched text.
- No English-language, real-victim (non-baiter), publicly documented transcript corpus with legitimate-call controls was identified; every strong-number dataset is synthetic, Korean, Chinese, or scam-baiter sourced.
- Industry vendors (Pindrop, Hiya, Truecaller, Nomorobo) publish no linguistic-feature studies that I could locate; the Pindrop "forensic linguistics" page was a customer case study with no linguistic content.
