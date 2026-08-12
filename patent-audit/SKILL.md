---
name: patent-audit
description: Audit a draft U.S. utility patent application before it is filed, against a 316-item checklist grounded in 35 U.S.C., 37 CFR, the MPEP, and current USPTO practice. Runs a deterministic pre-pass over the draft, gates on patentability, inventorship and deadlines, then fans out parallel review agents over the specification, claims, drawings and filing packet, adversarially verifies every fatal finding, and reports ranked defects with honest coverage accounting. Use when asked to audit, review, check, or pre-flight a patent application, provisional, specification, or claim set before filing.
---

# Pre-filing patent application audit

Audit a draft utility patent application against 316 checklist items and return a
ranked defect list with coverage accounting.

**Not legal advice.** The checklist is grounded in 35 U.S.C., 37 CFR, the MPEP,
and current USPTO materials. Fee amounts, form names and filing mechanics must
be re-verified against current PTO practice, and §101 case law moves. Say so
in the report; the template already does.

## What ships with this skill

| Path | Purpose |
|---|---|
| `reference/checklist_index.json` | All 316 items with routing: `id, part, section, title, check, severity, applies_to, inputs, automation, owner, blocking` |
| `reference/parts/{A..I}_*.md` | Full item text per part — **these are the agent payloads** |
| `scripts/prepass.py` | One command for all of Phase 1 |
| `scripts/parse_application.py` | Draft → structured `parsed.json` |
| `scripts/mechanical_checks.py` | Deterministic checks → `findings_mechanical.json` |
| `scripts/deadlines.py` | Intake → `deadlines.json` with weekend/holiday rollover |
| `scripts/synthesize.py` | All findings → ranked report + coverage |
| `assets/intake.yaml` | The intake questionnaire template |
| `assets/sample_draft.md` | A draft with planted defects, for testing the harness |

Routing is precomputed. Every item carries:

- **`inputs`** — what evidence it consumes: `draft_text` (210 items), `intake_facts` (99),
  `forms_packet` (68), `drawings` (47), `search_report` (40), `prior_art_refs` (20),
  `ppa_text` (20), `parent_app` (13).
- **`automation`** — `mechanical` (28), `assisted` (169), `judgment` (119).
- **`owner`** — which agent runs it.
- **`blocking`** — 105 items halt the audit on failure.

**26 items are answerable only from intake facts.** No document review reaches them:
`A19 A20 A22–A25 A36 C05 C08–C12 C21 D19–D26 D28 D29 I38 I42`. If intake is
skipped, those are `cannot_assess` — never `pass`.

## Core principles

**The draft fits in one context. Parallelize for attention, not capacity.** Every
agent gets the whole application. Never chunk the document across agents —
enablement, antecedent basis and numeral consistency are whole-document properties.

**Never let a model do arithmetic or exhaustive cross-referencing.** Dates, claim
counts, fee tiers, dependency graphs and numeral reconciliation run in code. Models
find 19 of 20 numerals and report "all consistent."

**Silence is not a pass.** Every item ends as `pass`, `fail`, `cannot_assess`,
`not_applicable`, or `not_reached`. An agent that omits an item has not passed it.

**`cannot_assess` is a correct answer.** Some items — the duty of candour above all
— cannot be established from any document. Guessing is worse than admitting.

---

## Phase 0 — Intake (blocking)

Run `prepass.py` with no `--intake`; it writes the questionnaire into the working
directory. Have the user fill it. Parts A, C and D are unanswerable without it.

Do not proceed past the gates on assumed facts. If the user wants to start anyway,
run Phases 1 and 3 only, and mark every intake-dependent item `cannot_assess`.

The most consequential fields are the disclosure and bar dates, and
`disclosure_made_by` — post-AIA, only an inventor-derived disclosure gets the
one-year grace period. A third party's independent disclosure before filing means
the U.S. right is already gone, and no amount of drafting fixes it.

## Phase 1 — Deterministic pre-pass

```bash
python scripts/prepass.py --draft DRAFT --drawings DRAWINGS \
    --intake intake.yaml --workdir audit_run
```

Exit 1 means intake is missing; exit 2 means the draft did not parse and the run
must stop. Individual steps if you need them:

```bash
python scripts/parse_application.py DRAFT --drawings D -o parsed.json
python scripts/mechanical_checks.py parsed.json --intake intake.yaml -o findings/findings_mechanical.json
python scripts/deadlines.py intake.yaml -o deadlines.json [--asof YYYY-MM-DD]
```

`parse_application.py` accepts `.txt`, `.md`, `.pdf`, `.docx`. `prepass.py` refuses
to continue when no claims parsed, fewer than four sections were recognised, or the
detailed description yielded no reference numerals — all signs the draft uses
headings the parser did not expect. Fix the parse before dispatching agents;
otherwise they confidently audit a document that isn't there.

The mechanical checks credit the checklist items they cover, so those items are not
reported as unaudited. A mechanical `pass` never suppresses a later agent `fail` on
the same item — the synthesizer keeps the worst verdict.

Hand `parsed.json` to every agent. It carries the claim dependency graph, element
decomposition, antecedent-basis candidates, reference-numeral tables and figure
inventory, so no agent has to recompute them.

## Phase 2 — Gates (sequential, fail fast)

Run in order. Each gets `intake.yaml`, `parsed.json`, `deadlines.json`, the draft,
and only its own part file.

| Agent | Part file | Also needs |
|---|---|---|
| `gate_threshold` | `A_threshold.md` | search report, closest prior art |
| `gate_inventorship` | `C_inventorship.md` | — |
| `gate_priority` | `D_priority_deadlines.md` | `deadlines.json`, PPA text, parent |

**If any gate returns a `fail` on an item tagged `blocking: true`, stop.** Report
the blocker and do not spend tokens auditing the prose of an application that is
statutorily barred, names the wrong inventors, or has already lost its priority
date. Tell the user what would have run.

`gate_priority` must not compute dates. `deadlines.json` already has them, with
rollover applied. Its job is to interpret them and catch the conflicts the script
flags in `warnings`.

## Phase 3 — Document fan-out (parallel, single message)

Eight agents, all with the full draft and `parsed.json`. Launch together.

| Agent | Part file | Lens to put in the prompt |
|---|---|---|
| `doc_enablement` | `E_disclosure.md` (own items) | Read as a skilled artisan *trying to build it*. Every point where you'd have to invent something is a gap. |
| `doc_narrowing` | `E_disclosure.md` + `F_spec_sections.md` (own items) | Read as opposing counsel hunting for admissions, essentiality language, and claim-construction traps. |
| `doc_spec_sections` | `F_spec_sections.md` | Walk the spec section by section in PTO order. |
| `doc_claims_law` | `G_claims.md` (own items) | §112 form, definiteness, antecedent basis, means-plus-function. Adjudicate the `candidates` lists from the mechanical pass — do not re-derive them. |
| `doc_claims_arch` | `G_claims.md` (own items) | Set architecture: is claim 1 the broadest? Does each dependent add real scope? Are the statutory classes covered? |
| `doc_drawings` | `H_drawings.md` + I05, I33 | **Multimodal — attach the sheets as images.** Text-only, this agent silently passes. |
| `doc_filing` | `I_filing_packet.md` | Formalities, ADS, declaration, fees, IDS, nonpublication request. |
| `doc_search` | `B_search.md` | Was the search adequate, were the references read correctly, does the draft answer what was found? |

Split `E`/`F`/`G` between their agents using the `owner` field in
`checklist_index.json`, not by file — owners deliberately cross file boundaries. An
item about narrowing language belongs to `doc_narrowing` wherever it sits, and the
claim-support items in Part G belong to `doc_enablement`.

Filter each agent's payload to its own IDs:

```bash
python -c "import json,sys; \
 ids={i['id'] for i in json.load(open('reference/checklist_index.json',encoding='utf-8')) \
      if i['owner']==sys.argv[1]}; print(' '.join(sorted(ids)))" doc_narrowing
```

Workload is uneven by design: `gate_priority` 48, `doc_filing` 46,
`doc_claims_law` 39, `gate_threshold` 35, `doc_enablement` 25, `doc_drawings` 24,
`doc_claims_arch` 23, `doc_search` 22, `gate_inventorship` 21,
`doc_spec_sections` 19, `doc_narrowing` 14.

### Red team (launch with the same batch)

The highest-value output, and not checklist-shaped. Each returns prose, not findings.

- **`redteam_examiner`** — You are the examiner. Given these claims and this search
  report, write the first Office Action you would actually issue: every §101, §102,
  §103 and §112 rejection, with the reference and the mapping.
- **`redteam_design_around`** — Given claim 1, design three products that capture
  the commercial value and do not infringe. If this is easy, claim 1 is too narrow —
  no checklist item will tell you that.
- **`redteam_invalidity`** — Assume it issued and you are the accused infringer.
  Attack it: priority defects, §112 gaps, prior art the applicant missed.

## Phase 4 — Adversarial verification

For **every** `fail` on a `blocking` item, spawn a fresh verifier that receives the
draft and the claim **but not the finding's reasoning**, and is prompted to refute
it. Three verifiers; the finding survives on two. Record survivors in the finding's
`verified_by` field and drop the rest to `cannot_assess` with a note.

This is where surplus budget goes. A 93-item fatal list with a 20% false-positive
rate is worse than a clean 60-item list — attorneys stop reading audits that cry wolf.

## Phase 5 — Synthesis

```bash
python scripts/synthesize.py findings/ --deadlines deadlines.json \
    -o audit_report.md --json audit_report.json
```

Exits non-zero when a fatal item failed. Reports `not_reached` for any item no agent
touched — check that number is zero before calling the audit complete. If it isn't,
an agent skipped work; re-run that agent.

Append the three red-team outputs as appendices.

---

## Finding schema

Every agent returns **only** a JSON array to `findings/<agent>.json`. No prose.

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

`verdict` ∈ `pass | fail | cannot_assess | not_applicable`. Rules to put in every
agent prompt:

1. Emit exactly one entry per item in your part file. Count them before writing.
2. `evidence` must be a **verbatim quote from the draft**, never a paraphrase. A
   finding with no quote is not a finding.
3. Use `cannot_assess` when the input is missing. Never infer a date, an inventor's
   knowledge, or a fact not in the materials.
4. `not_applicable` needs a reason in `explanation`.
5. Do not edit the draft. This is an audit; remediation is a separate pass.

## Scaling

Typical case (20–60 pages, ~20 claims): 11 agents in Phase 3, wall clock ≈ the
slowest, 5–10 minutes. Large claim sets (100+) — fan `doc_claims_law` out per claim,
since form checks are claim-independent; keep `doc_claims_arch` whole-set.

## Do not

- Run one agent per checklist item. 316 agents each re-reading the draft buys
  nothing; items share reading effort.
- Chunk the draft across agents.
- Let an audit agent edit the draft — you lose the evidence trail.
- Report a `pass` for anything an agent stayed silent about.
- Recompute in a model what `parsed.json` already computed exactly.
