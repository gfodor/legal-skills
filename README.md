# legal-skills

**Replace billable hours with markdown files and an AI that actually follows them.**

This repository is a public, executable playbook for U.S. utility-patent work. Not a chatbot wrapper. Not a "talk to a lawyer" landing page. A set of agent skills — `SKILL.md` files, checklists, examiner/adversary protocols, intake questionnaires, and deterministic Python — that make a language model do the work a patent boutique currently invoices at several hundred dollars an hour.

The goal is not to "assist" counsel. The goal is to **displace legal fees**. If an inventor, founder, or in-house engineer can run a 316-item pre-filing audit, a simulated USPTO prosecution loop, and an adversarial design-around attack without opening a matter, that is a win. If a firm that used to charge $18,000 to draft and file a utility application is now competing with a checkout of this repo and a model that costs less than lunch, that is also a win.

Lawyers who are good at judgment, strategy, and courtroom work will still have work. Lawyers whose product is walking a known statute, filling known forms, and billing the walk — this repo is aimed at that product.

---

## This is not legal advice

**Read this before you use anything in this repository.**

This project is **not a law firm**. It does not create an attorney–client relationship. Nothing here is legal advice, a legal opinion, a patentability opinion, an infringement opinion, a freedom-to-operate opinion, or a representation that any application will be allowed, valid, enforceable, or commercially useful.

- These skills **do not file** applications, **do not sign** inventor declarations, **do not submit** Information Disclosure Statements, **do not contact** the USPTO, and **do not appear** before any tribunal.
- Outputs are **AI simulations** grounded in 35 U.S.C., 37 CFR, the MPEP, current official USPTO texts the agent is instructed to re-fetch, and whatever facts you put in the intake. Models hallucinate cites, miss art, and invent confidence. The scripts exist because models also cannot count, cannot do date arithmetic, and will report "all numerals consistent" after finding 19 of 20.
- Fee amounts, form names, PTO mechanics, and §101 case law **move**. The audit checklist is a primary-source pre-filing checklist — statutes, rules, MPEP, and current Office practice — not a substitute for the official text. The examination and workaround skills require the agent to refresh statutes, rules, MPEP pages, and examination memoranda on every run. Verify those sources yourself before you rely on a result.
- Some acts remain reserved to a human with the right credentials: signing a declaration under penalty of perjury, making the ultimate duty-of-candor / IDS materiality call, recording an assignment, paying the PTO, and anything that requires a registered practitioner. The skills **refuse** to do those things without your separate, explicit authorization, and even then they will not pretend they *are* you.
- **You** own the consequences. A bad claim set, a missed statutory bar, a false entity-status claim, or an omitted material reference can destroy rights. If the stakes are high enough that you would sue someone over a missed deadline, hire a registered practitioner and use this repo as the thing that makes that person cheaper, faster, and harder to snow.

The GPL-3.0 license already disclaims warranty. This paragraph is the same idea in English: **use at your own risk.**

That disclaimer is required because the work is real enough to hurt you if you treat it as magic. It is **not** a retreat from the pitch. The pitch is that most of what you were paying for was process, and process belongs in files.

---

## Why markdown, not a firm

Patent work is already a document pipeline:

1. Facts that are not in the draft (disclosure dates, inventorship, entity status).
2. A specification and claims that either enable the invention or do not.
3. A search that either found the dead-ringer or did not.
4. An examiner who will reject under 35 U.S.C. 101 / 102 / 103 / 112 until the claims are allowable or you give up.
5. A competitor who will keep the value proposition and drop the limitation you accidentally treated as essential.

Firms wrap that pipeline in scarcity, letterhead, and a rate card. This repo unwraps it.

| What you used to buy | What this repo is |
|---|---|
| A $400/hr associate reading the draft once | 11 specialized agents, each with the **whole** application and a part-file of checklist items they are forbidden to skip |
| A partner "doing the claims" from muscle memory | A 64-item claims part, a mechanical parser that builds the dependency graph, and a red-team examiner who has to write a real Office Action |
| A design-around "gut check" in a conference room | Fresh competitor subagents plus an outer-agent umbrella classification that will not let you claim a result you did not disclose |
| An invoice | `git clone` |

The files are the product. If a better model ships next quarter, the same files get cheaper and sharper. If the PTO changes a form, you edit a markdown file instead of waiting for a CLE.

---

## What's here

Three skills. They are designed to be run in order. Each one is a complete agent skill: a `SKILL.md` the orchestrator reads as its contract, plus the payloads, templates, and scripts that keep the model honest.

```
legal-skills/
├── patent-audit/         Pre-filing audit. 316 checklist items. Deterministic pre-pass.
├── patent-examine/       Recurrent simulated USPTO examination until two independent examiners clear the same version.
├── patent-workaround/    Adversarial design-around testing. Strengthen only what is supported and patentable.
├── LICENSE               GNU GPL v3
└── README.md             This file
```

**Suggested pipeline**

```
     inventor facts + draft
              │
              ▼
      ┌───────────────┐
      │ patent-audit  │  Is this even fileable? Stop on statutory bars.
      └───────┬───────┘
              │ ranked defects + parsed.json
              ▼
      ┌───────────────┐
      │patent-examine │  Mock prosecution. Amend only after a simulated OA.
      └───────┬───────┘
              │ version-locked "allowable" candidate
              ▼
      ┌──────────────────┐
      │patent-workaround │  Can a competitor keep the value and miss the claims?
      └────────┬─────────┘
               │
               └── iterate examine ↔ workaround until two examiners
                   and two adversaries clear the same packet
```

`patent-examine` and `patent-workaround` will use `patent-audit`'s parser and mechanical checks if that sibling skill is installed. A prior audit is **not** a substitute for examination. A prior examination is **not** a substitute for workaround testing.

---

## Install

These are [agent skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills): a directory with a `SKILL.md` the model is instructed to follow. Copy the three skill folders into the skills directory of whatever agent you run.

| Agent | Typical location |
|---|---|
| Grok | `~/.grok/skills/` |
| Claude Code | `~/.claude/skills/` or project `.claude/skills/` |
| Codex / Cursor / other skill hosts | that product's skills directory |

On Windows, from this repo:

```powershell
Copy-Item -Recurse .\patent-audit, .\patent-examine, .\patent-workaround $HOME\.grok\skills\
```

Then tell the agent, in plain language:

- *Use `$patent-audit` to audit this draft before I file it.*
- *Use `$patent-examine` until two fresh examiners independently find the same version allowable.*
- *Use `$patent-workaround` to pressure-test this draft against credible design-arounds.*

Python 3 is required for the scripts. The audit parser accepts `.txt`, `.md`, `.pdf`, and `.docx`. PDF needs [PyMuPDF](https://pymupdf.readthedocs.io/); `.docx` needs [python-docx](https://python-docx.readthedocs.io/). Missing optional dependencies fail loudly instead of silently producing a half-parse. The state lockers (`cycle_state.py`, `coverage_state.py`) use only the standard library.

Do not point a model at the draft and skip the skill. The value is the protocol, not "an LLM that has heard of patents."

---

## `patent-audit` — pre-filing audit

**When:** before you file a utility application, a provisional, or a claim set you are about to spend money on.

**What it returns:** a ranked defect list with honest coverage accounting — every item is `pass`, `fail`, `cannot_assess`, `not_applicable`, or `not_reached`. Silence is never a pass.

**What it is not:** a rewrite of the application. Audit agents are forbidden to edit the draft. Remediation is a later pass.

### The 316-item checklist

The checklist is a primary-source pre-filing audit of a U.S. utility draft — 35 U.S.C., 37 CFR, the MPEP, and current USPTO practice — not a vibe. Every item has an id, part, severity, owner agent, input types, automation class, and a `blocking` flag. Routing is precomputed in `reference/checklist_index.json`. The full item text lives in `reference/parts/` — those files **are** the agent payloads. Each item body cites a statute, rule, MPEP section, or current official page.

| Part | File | Items | Fatal | What it actually checks |
|---|---|---|---|---|
| A | `A_threshold.md` | 37 | 18 | Is this patentable **at all**? §101 class + judicial exceptions, utility, novelty, statutory bars, nonobviousness. The "don't file" gate. |
| B | `B_search.md` | 22 | 1 | Was the search real? Classes **and** keywords, NPL, foreign docs, citation chaining, reading references as disclosures, IDS queue. |
| C | `C_inventorship.md` | 21 | 9 | Who conceived a claimed limitation? Employment agreements, shop rights, joint-owners agreements, assignments, utility vs design vs plant. |
| D | `D_priority_deadlines.md` | 46 | 16 | PPA enablement, one-year conversion, foreign rights, NPR conflicts, continuation/divisional/CIP labeling, double patenting, term. |
| E | `E_disclosure.md` | 27 | 8 | Enablement, written description, best-mode *without naming a favorite*, software listings/flowcharts, patent profanity, no-new-matter completeness. |
| F | `F_spec_sections.md` | 29 | 3 | PTO section order, Background that does not confess the invention, numeral hygiene, structure-then-operation, ramifications, 150-word abstract. |
| G | `G_claims.md` | 64 | 17 | Breadth vs prior art, antecedent basis, means-plus-function support, single-means ban, method-actor unity, CRM claims, claim count/fees. |
| H | `H_drawings.md` | 22 | 3 | Every claimed feature shown, no new-matter holes, OPAP formalities, line types, color/photo petitions. **Multimodal — sheets must be attached as images.** |
| I | `I_filing_packet.md` | 48 | 17 | Declaration/ADS consistency, entity status, IDS, NPR, EFS-Web vs paper, PME, fee arithmetic, form versions. |

**316 items.** 105 are `blocking` — a fail on one of those stops the audit. 28 are `mechanical` (code). 169 are `assisted` (model + structured evidence). 119 are `judgment`.

**26 items can only be answered from intake facts.** No amount of document review reaches them (disclosure/bar dates, inventorship knowledge, duty of candor, some foreign and fee facts). If you skip intake, those come back `cannot_assess`. That is the correct answer. Guessing a first-public-disclosure date is how people lose the U.S. right and then pay a lawyer to confirm they lost it.

### Core rules the orchestrator is not allowed to break

1. **The draft fits in one context.** Every agent gets the whole application. Enablement, antecedent basis, and numeral consistency are whole-document properties. Chunking the spec across agents is a bug.
2. **Models do not do arithmetic or exhaustive cross-references.** Dates, claim counts, fee tiers, dependency graphs, and numeral reconciliation run in Python.
3. **`cannot_assess` is a valid verdict.** Duty of candor cannot be established from any document. An agent that guesses has failed the skill.

### Phases

| Phase | What happens |
|---|---|
| **0 — Intake** | `prepass.py` with no `--intake` writes the questionnaire and stops. Fill it. Parts A, C, and D are unanswerable without it. |
| **1 — Deterministic pre-pass** | Parse → mechanical checks → deadline table. Exit 2 if the parse looks like the wrong document. |
| **2 — Gates (fail-fast)** | `gate_threshold` → `gate_inventorship` → `gate_priority`. A blocking fail **stops the run**. Do not spend tokens polishing prose on a barred application. |
| **3 — Document fan-out** | Eight specialist agents plus three red-team agents, launched together. |
| **4 — Adversarial verification** | Every blocking `fail` is re-tried by three fresh verifiers who see the draft and the claim **but not the finding's reasoning**. Survivors need 2 of 3. |
| **5 — Synthesis** | `synthesize.py` ranks defects and reports `not_reached`. If that count is not zero, an agent skipped work. |

### Phase 3 agents

| Agent | Owns | Lens |
|---|---|---|
| `doc_enablement` | Part E items (plus claim-support items in G) | Skilled artisan **trying to build it**. Every place you'd have to invent something is a gap. |
| `doc_narrowing` | Narrowing-language items across E/F | Opposing counsel hunting admissions, essentiality language, and claim-construction traps. |
| `doc_spec_sections` | Part F | Walk the spec in PTO order. |
| `doc_claims_law` | §112 form, definiteness, antecedents, 112(f) | Adjudicate the mechanical pass's `candidates` lists. Do not re-derive them. |
| `doc_claims_arch` | Claim-set architecture | Is claim 1 the broadest? Does each dependent add real scope? Are the classes covered? |
| `doc_drawings` | Part H + I05, I33 | **Attach the sheets as images.** Text-only, this agent silently passes. |
| `doc_filing` | Part I | ADS, declaration, fees, IDS, NPR. |
| `doc_search` | Part B | Was the search adequate, were the references read as disclosures rather than as claim sets? |

Split E/F/G by the `owner` field in `checklist_index.json`, not by file. Workload is uneven on purpose: `gate_priority` 48, `doc_filing` 46, `doc_claims_law` 39, `gate_threshold` 35, then down to `doc_narrowing` at 14.

**Red team (same batch, not checklist-shaped):**

- `redteam_examiner` — write the first Office Action you would actually issue.
- `redteam_design_around` — three products that keep the commercial value and miss claim 1. If this is easy, claim 1 is too narrow. No checklist item will tell you that.
- `redteam_invalidity` — assume it issued. Attack priority, §112, and the art the applicant missed.

### Scripts

```powershell
python patent-audit/scripts/prepass.py --draft DRAFT --drawings DRAWINGS `
    --intake intake.yaml --workdir audit_run
```

| Script | Job |
|---|---|
| `prepass.py` | One command for all of Phase 1. No `--intake` → write the questionnaire and stop. Exit 1 = missing intake. Exit 2 = parse refused. |
| `parse_application.py` | Draft → `parsed.json`: sections, claim dependency graph, element decomposition, antecedent-basis candidates, numeral tables, figure inventory. |
| `mechanical_checks.py` | Deterministic checks → `findings_mechanical.json`. A mechanical `pass` never suppresses a later agent `fail` on the same item. |
| `deadlines.py` | Intake → `deadlines.json` with weekend/holiday rollover. Agents **interpret** dates; they do not compute them. |
| `synthesize.py` | All findings → ranked report + coverage. Non-zero exit if a fatal item failed. |

`prepass.py` refuses to continue when no claims parsed, fewer than four sections were recognized, or the detailed description yielded no reference numerals. That is how you keep eleven agents from confidently auditing a document that isn't there.

### Finding schema

Every audit agent returns **only** a JSON array to `findings/<agent>.json`:

```json
[{
  "item_id": "G14",
  "verdict": "fail",
  "severity": "Serious",
  "location": "claim 3",
  "evidence": "the said locking member",
  "explanation": "No earlier claim introduces a locking member.",
  "suggested_fix": "Introduce 'a locking member' in claim 1, or recite it in claim 3.",
  "confidence": "high"
}]
```

`evidence` must be a **verbatim quote from the draft**. A finding with no quote is not a finding.

### Assets

- `assets/intake.yaml` — the questionnaire. Leave unknowns `null`. Null → `cannot_assess`.
- `assets/sample_draft.md` — a draft with planted defects, for testing the harness.

Typical wall-clock for a 20–60 page, ~20-claim case is the slowest Phase-3 agent, about 5–10 minutes. Claim sets of 100+ should fan `doc_claims_law` per claim; keep `doc_claims_arch` on the whole set.

---

## `patent-examine` — recurrent simulated examination

**When:** you want the draft stress-tested the way an examiner will actually attack it, then revised until two independent simulated examiners clear the **same** bytes.

**What it returns:** a version-locked prosecution record, a final ground-truth application, and a prominent statement that this was a simulation.

**What it is not:** a USPTO allowance, a validity guarantee, or a one-pass checklist. That last job is `patent-audit`.

### The state model (non-negotiable)

Three artifacts, kept separate:

1. **Ground truth** — the authoritative editable application. Frozen during an examiner dialogue.
2. **Proposed candidate** — a complete clean application containing the exact amendments on offer. Arguments alone may leave it byte-identical to ground truth. An examiner may clear **only** a complete candidate, never a promise to draft later.
3. **Prosecution record** — Office Actions, responses, interview summaries, reference copies, search logs, issue ledger, versions, hashes.

After a clearance, apply the candidate **verbatim** to ground truth and verify the content hash. Any unapproved substantive deviation voids the clearance.

```powershell
python patent-examine/scripts/cycle_state.py init --run-dir examination_run `
  --candidate application=application.docx --candidate drawings=drawings.pdf

python patent-examine/scripts/cycle_state.py snapshot --run-dir examination_run `
  --candidate application=proposal/application.docx `
  --candidate drawings=proposal/drawings.pdf

python patent-examine/scripts/cycle_state.py record --run-dir examination_run `
  --examiner examiner-01 --decision conditional-allowable `
  --document examination_run/examiner-01/notice-of-allowability.md

python patent-examine/scripts/cycle_state.py promote --run-dir examination_run `
  --candidate application=application.docx --candidate drawings=drawings.pdf

python patent-examine/scripts/cycle_state.py status --run-dir examination_run
```

### Phases

| Phase | What happens |
|---|---|
| **0 — Packet** | Intake. Completeness gate. Refresh official sources. Documented prior-art search. Missing material is `missing`, not a favorable fact. |
| **1 — Fresh examiner** | Spawn one subagent with a unique context ID and **no** prior examiner's reasoning. First merits response is a simulated non-final Office Action or `ALLOWABLE`. |
| **2 — Dialogue** | Same examiner until `CONDITIONAL_ALLOWABLE`, `ALLOWABLE`, or a genuine terminal impasse. Outer agent independently validates every 102/103 mapping. |
| **3 — Promote** | Apply the cleared candidate. Re-render the whole application. Re-run mechanical checks. `promote` must hash-match. |
| **4 — Repeat** | A **different** fresh examiner. Zero qualifying clearances if the application changes. Success = **two** distinct examiners independently clear the **same** promoted hash. |

### Prior-art substance gate

The outer agent does not accept the examiner's chart on faith. For every 102/103 ground it reads the full claim, the full reference, and reconstructs both arrangements in technical terms. Mapping modes are `express`, `inherent`, `proposed 103 modification`, or `POSITA knowledge/evidence`. Similar words are not a mapping.

If the mapping looks wrong, the outer agent sends `PRIOR_ART_ACCURACY_CHALLENGE` **before** narrowing the claims. The examiner must `CONCUR_AND_WITHDRAW`, `CORRECT_OR_MODIFY`, or `MAINTAIN_WITH_SUPPORT`. Examiner agreement is useful, not dispositive. Protocol failure (ignoring the challenge, silently changing theories) closes that cycle with **zero** clearance credit.

Do not amend to overcome an unsupported rejection before testing whether the rejection is actually supported. That is how people donate scope.

### Examiner decisions

Exact top-line tokens, from `references/examiner-protocol.md`:

- First action: `SIMULATED_NONFINAL_OFFICE_ACTION` | `ALLOWABLE` | `INCOMPLETE`
- Later: `CONTINUED_EXAMINATION` | `CONDITIONAL_ALLOWABLE` | `ALLOWABLE` | `INCOMPLETE` | `TERMINAL_IMPASSE`

`INCOMPLETE` is the right first move when claims are unreadable, drawings needed to understand the disclosure are missing, or effective-filing-date facts are too thin to know which art applies. Do not ask that examiner to "just search anyway."

For a pre-filing draft, the planned nonprovisional filing date is used; if none is supplied, the run date is an expressly hypothetical conservative AIA filing date. That assumption enables the simulation. It does **not** establish a legal priority date.

### What ships with the skill

| Path | Purpose |
|---|---|
| `references/examiner-protocol.md` | Examiner's identity, independence, evidentiary rules, clearance contract |
| `references/office-action-format.md` | OA structure, minimum support per statute, applicant-response rules |
| `references/official-sources.md` | Source hierarchy: 35 U.S.C. → 37 CFR → precedent → MPEP → search databases |
| `assets/examination-intake.yaml` | Run facts. Do not infer. |
| `assets/examiner-handoff.md` | What a fresh examiner is allowed to see |
| `assets/prior-art-validation.md` | Outer-agent substance gate + accuracy-challenge template |
| `assets/applicant-response.md` | Response / redline / support-map template |
| `scripts/cycle_state.py` | Hash-locked init / snapshot / record / promote / status |

Termination as **blocked** (not success) when essential evidence is unavailable, the only cure is unsupported new matter, a statutory/priority defect is not curable by drafting, or a required inventor decision is missing. Token pressure is not a success condition.

---

## `patent-workaround` — adversarial design-around testing

**When:** you want to know whether a competent competitor can keep the product and miss the claims — and whether the gap belongs **inside** the invention you actually made.

**What it returns:** a coverage ledger, a claim/disclosure amendment package that survived support and patentability gates, and a list of deliberate gaps you chose to live with.

**What it is not:** an infringement opinion, an FTO opinion, or proof that "no one can design around this." Two qualifying adversaries is an exhaustion rule for the workflow, not a market forecast.

### Five distinctions the skill will not let you collapse

| Question | Meaning |
|---|---|
| **Claim coverage** | Does every limitation of at least one relevant claim appear to be met? A legal-scope **hypothesis**, not a verdict. |
| **Workaround credibility** | Does the alternative still deliver the material value? Deleting the product is not a workaround. |
| **Umbrella alignment** | Does this alternative belong in the intended patent family, given the motivating problem, design objectives, disclosed mechanism, and deployed implementation? Strategic, not legal. |
| **Disclosure support** | What does the authoritative application actually teach? Business intent is not written description. |
| **Patentability** | Would a capture claim survive current 101/102/103/112 scrutiny? A real commercial gap can be unclaimable. |

Do not say a workaround is "covered by the patent" because it shares a theme. Exclusionary scope comes from claims and applicable law.

### Classification vocabulary

After independent verification, each candidate is one of:

- `not-a-workaround` — captured, implausible, or value-destroying
- `outside-umbrella` — credible avoidance of a different invention
- `umbrella-gap-supported` — inside the intended contribution and supported enough to consider capture
- `umbrella-gap-unsupported` — strategically aligned, **not** possessed/enabled by the disclosure. **Blocks** a qualifying disposition even if you are willing to tolerate it.
- `cannot-assess`

Absence from the disclosure does **not** by itself place an alternative outside the umbrella. That fact controls the support gate, not the strategy gate.

### Attack matrix (what the adversary must try)

The competitor subagent is a product architect, not a drafter. It does not propose claim amendments. It does not see the invention-thesis map, the coverage ledger, or the capture strategy. It must generate enough alternatives to cover the viable lenses, then fully develop **at least five** materially distinct candidates unless fewer are technically credible:

1. omit an element or make it optional
2. substitute structure / material / algorithm / signal
3. change topology, control locus, or component boundary
4. split steps across actors, services, locations, jurisdictions
5. change order, timing, triggering, persistence
6. move work to pre/post-processing, training, manufacture, or the user
7. swap automation ↔ human action
8. move between centralized / distributed / edge / cloud / embedded
9. deliver the outcome through a different statutory class
10. exploit a claimed threshold, range, sequence, or exclusivity
11. combine known public technology around the asserted mechanism
12. test whether another independent claim still captures the result

Decisions: `GAPS_FOUND` | `NO_MATERIAL_GAP` | `INCOMPLETE`.

### Integration order (what the outer agent is allowed to change)

Stop at the first defensible remedy:

1. Fix a genuine construction or consistency defect.
2. Revise or add a **supported** independent claim aimed at the inventive mechanism (including parallel method / system / device / CRM classes when justified).
3. Add supported dependent fallbacks.
4. Improve the summary or detailed description with supported alternatives — narrative is not a claim.
5. Flag a continuation / CIP / reissue / separate filing as a **counsel** question. Do not assume priority or inventorship.
6. Record a deliberate gap when capture would add new matter, collide with art, or exceed the invention.

For a pending application, every amendment maps to the application **as filed**. For a pre-filing draft, new technical content comes only from authentic inventor-supplied facts, labeled for inventor confirmation. **Never fabricate an embodiment to close a gap.** An issued patent is a different posture; do not rewrite it as a draft.

For a pending case, potentially material information discovered in search or attack is routed to a qualified human for IDS/timing triage. The AI does not make the ultimate disclosure decision. Unresolved triage **blocks promotion**.

### State locker

```powershell
python patent-workaround/scripts/coverage_state.py init --run-dir workaround_run `
  --candidate application=application.docx --candidate drawings=drawings.pdf `
  --candidate intake=intake.yaml --candidate thesis=invention-thesis.md `
  --candidate search=search-record.md --candidate evidence=evidence-bundle.zip `
  --authoritative application --authoritative drawings
```

Required packet labels: `application`, `intake`, `thesis`, `search`, `evidence`. `drawings` is optional at init and cannot later be silently added or omitted. Qualifying pair is `NO_MATERIAL_GAP` → `no-material-gap`, or `GAPS_FOUND` → `only-accepted-gaps`. Two distinct fresh adversaries on the **same** packet hash, then `promote`. Any material input change resets the count.

`scripts/test_coverage_state.py` is the unit test for that locker. Run it when you change the script.

### What ships with the skill

| Path | Purpose |
|---|---|
| `references/workaround-protocol.md` | Adversary identity, attack matrix, report headers the state tool will reject if wrong |
| `references/integration-gates.md` | Eight outer-agent gates: credibility → coverage → umbrella → support → capture → patentability → narrative → promotion |
| `references/current-sources.md` | Law + claim-scope + prior-art source hierarchy (includes infringement doctrines the MPEP will not decide for you) |
| `assets/workaround-intake.yaml` | Run facts, including IDS-triage fields |
| `assets/invention-thesis.md` | Evidence-cited map of problem / objectives / mechanism / deployed solution |
| `assets/adversary-brief.md` | Redacted brief. Full thesis and capture strategy stay with the outer agent. |
| `assets/adversary-handoff.md` | Dispatch contract |
| `assets/coverage-ledger.md` | Living chart of every candidate |
| `assets/outer-adjudication.md` | Disposition document the state tool validates |
| `assets/search-record.md` | Queries, dates, full references, materiality routing |
| `assets/evidence-manifest.json` | Hashed evidence bundle inventory |
| `scripts/coverage_state.py` | Packet hashes, dual-stage record, promotion |

---

## What these skills will not do

- Practice law, form an attorney–client relationship, or carry malpractice insurance for you.
- File, sign, pay, or correspond with the USPTO.
- Invent inventor facts, disclosure dates, or embodiments.
- Treat a clean search as proof of novelty. Unpublished applications exist.
- Treat two simulated allowances as a grant.
- Treat two failed design-arounds as an injunction against the industry.
- Audit a drawing set from text alone.
- Credit a `pass` for an item nobody touched.
- Let you claim small-entity or micro-entity status because it would be cheaper.

If you need someone to put their registration number on a transmittal, hire that person. Hand them the audit report, the prosecution record, and the coverage ledger. That is still an order of magnitude cheaper than paying them to *discover* the defects these files already know how to find.

---

## Source discipline

The audit checklist is written against 35 U.S.C., 37 CFR, the MPEP, and current USPTO pages, item by item. Those sources still move. The examination and workaround skills require a refresh of:

1. **35 U.S.C.** from the House Office of the Law Revision Counsel
2. **37 CFR Part 1** on eCFR
3. Binding Supreme Court and Federal Circuit opinions
4. Current MPEP + later examining-corps memoranda
5. Primary prior-art copies (USPTO Public Search, Patent Center, PATENTSCOPE, Espacenet, dated NPL)

Google Patents is a discovery tool. It is not a cite. Unverified aggregator hits are leads. They are not anticipation.

---

## License

[GNU General Public License v3.0](LICENSE).

Copy it. Fork it. Improve the checklist when the law moves. Charge money for running it if you want — the GPL allows that. What you may not do is take these files proprietary and sell the walk back to the people this repo exists to stop charging.

If you are a lawyer who thinks this is reckless: good. File an issue with a pinpoint cite and a better item. That is how this gets sharper than any one firm's form file.

If you are an inventor who was about to spend a year's runway on a first Office Action: start with `patent-audit`. Fill the intake. Do not skip the dates.
