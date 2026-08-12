---
name: patent-examine
description: Iteratively examine and revise a draft U.S. utility patent application through prosecution-style dialogues with fresh subagents role-playing USPTO examiners. Each examiner performs a current-law and prior-art review, issues Office-Action-style rejections or requirements under 35 U.S.C. 101, 102, 103, 112 and related grounds, then reconsiders exact applicant arguments and proposed amendments until all issues are resolved. Apply an examiner-approved amendment package to the ground-truth application only after that examiner indicates allowability, and repeat until two independent fresh examiners clear the same final version. Use for simulated examination, mock prosecution, rejection-response iteration, or examiner stress-testing of a patent draft; not for a one-pass pre-filing checklist audit.
---

# Recurrent simulated patent examination

Run a version-controlled applicant/examiner dialogue. Keep the main agent in the
applicant/drafter role and one persistent subagent in the examiner role per cycle.
Do not describe the result as an actual USPTO allowance or a guarantee of validity.

## Read before acting

Read all of these files:

- `references/examiner-protocol.md` for the examiner's role and decision contract.
- `references/office-action-format.md` for rejection sufficiency and response rules.
- `references/official-sources.md` for the current-law and prior-art source hierarchy.

Copy and complete `assets/examination-intake.yaml`. Use
`assets/examiner-handoff.md`, `assets/prior-art-validation.md`, and
`assets/applicant-response.md` in every cycle.

If the sibling `../patent-audit` skill is installed, read its `SKILL.md` and use its
deterministic pre-pass to produce `parsed.json`, mechanical findings, claim
dependencies, and date calculations. Re-run that pre-pass after claim or
specification amendments that can affect its outputs. Do not treat a prior audit as
a substitute for this examination loop.

## Non-negotiable state model

Maintain three separate artifacts:

1. **Ground truth**: the authoritative editable application. Do not change it during
   an examiner dialogue.
2. **Proposed candidate**: a full clean application containing the exact amendments
   being offered to the current examiner. Arguments alone may leave it byte-for-byte
   identical to the ground truth.
3. **Prosecution record**: Office actions, applicant responses, interview summaries,
   reference copies, search logs, issue ledger, versions, and hashes.

An examiner may conditionally clear only a complete proposed candidate, never a
promise to draft language later. After clearance, apply that candidate verbatim to
the ground truth and verify the content hash. Any unapproved substantive deviation
voids that clearance and must return to the same examiner or a fresh cycle.

Use `scripts/cycle_state.py` to make the version lock auditable. Label each component
consistently so proposal and ground-truth hashes compare correctly:

```powershell
python scripts/cycle_state.py init --run-dir examination_run `
  --candidate application=application.docx --candidate drawings=drawings.pdf

python scripts/cycle_state.py snapshot --run-dir examination_run `
  --candidate application=proposal/application.docx `
  --candidate drawings=proposal/drawings.pdf

python scripts/cycle_state.py record --run-dir examination_run `
  --examiner examiner-01 --decision conditional-allowable `
  --document examination_run/examiner-01/notice-of-allowability.md

# Apply the cleared files to the real ground truth, then verify rather than copy:
python scripts/cycle_state.py promote --run-dir examination_run `
  --candidate application=application.docx --candidate drawings=drawings.pdf

python scripts/cycle_state.py status --run-dir examination_run
```

Use the relevant document/PDF tooling to preserve layout, tracked changes, claim
numbering, equations, and drawings. Never edit a PDF extraction and call it the
source document.

## Phase 0 - Build the examination packet

Create a dedicated run directory. Preserve the user's original and identify the
editable ground truth. Complete the intake without guessing. Request or locate, as
applicable:

- the complete specification, claims, abstract, drawings, sequence listings, and
  appendices;
- filing, priority, benefit, continuity, inventorship, disclosure, sale/use, and
  AIA/pre-AIA facts;
- related applications and patents, IDS materials, cited art, search reports, and
  prosecution history;
- full copies of material patent and non-patent references with publication dates;
- declarations, test data, unexpected-results evidence, and claim-construction facts;
- commercial objectives, indispensable claim scope, and supported fallback positions.

Missing material is not a favorable fact. Mark it `missing` and distinguish
`cannot assess` from `no rejection found`.

Before dispatching a merits examiner, run a completeness gate. If the record lacks
material needed to establish what is being examined or which prior-art framework
applies—such as readable claims/specification, drawings necessary to understand the
disclosure, or enough filing/priority facts to assign effective dates—send a bounded
preliminary packet and require an immediate `INCOMPLETE` decision. Do not ask that
examiner to perform an exhaustive merits search that cannot yield a valid clearance.
Use its deficiency list to obtain the missing material; if the material is declared
unavailable, terminate blocked with zero clearance credit.

For a pre-filing draft, use the planned nonprovisional filing date. If none is
supplied, use the run date as an expressly hypothetical conservative filing date and
apply the AIA framework; do not credit an asserted earlier priority/benefit date
without the supporting application and claim-by-claim support. This assumption
enables a simulation only and does not establish a legal priority date or deadline.

Refresh the legal source record at the start of the run. Browse current official
statutes, rules, MPEP pages, examination memoranda, and technology-specific guidance.
Record URLs, revision/effective dates, access date, and which framework applies to
this application's dates. Use the source hierarchy in `official-sources.md`.

Perform or update a documented prior-art search before the first merits decision.
Search the claim as a whole and its inventive concepts, synonyms, CPC/USPC classes,
inventors/assignees, citations, and relevant non-patent literature. Preserve the
queries, databases, dates, classifications, and full references. A simulated
examiner who did not search cannot honestly clear novelty or nonobviousness.
Run search in staged passes and return a supported action using the best verified art
at hand; do not defer the action indefinitely in pursuit of an unknowable exhaustive
search. State coverage limits and continue searching after amendments when needed.

## Phase 1 - Start one fresh examiner cycle

Create a unique examiner context ID such as `examiner-01`. Spawn one subagent with a
fresh context and no prior examiner's discussion or conclusions. Provide only:

- the frozen ground-truth version and its version ID/hash;
- the completed handoff and intake;
- drawings as viewable images as well as source files when relevant;
- priority/continuity documents and prosecution history;
- known art, full reference copies, and the search log;
- `examiner-protocol.md`, `office-action-format.md`, and current official-source notes.

Tell the examiner not to inspect other examiners' run folders. The examiner must
independently construe the claims, search further when tools permit, and evaluate
every pending claim. Use the same subagent for all follow-up turns in this cycle;
do not replace it merely because it maintains a rejection.

The examiner's first merits response must be a simulated non-final Office Action or
an `ALLOWABLE` decision in the prescribed format. It must identify every claim's
status and every rejection, objection, restriction/election issue, or requirement
supported by the record. Citation and limitation mapping are mandatory for prior-art
grounds. A cite is not a mapping: the examiner must explain what the reference
actually teaches in context and how the relied-on embodiment, arrangement, and
operation meet the claim under the stated construction.

## Phase 2 - Conduct the applicant/examiner dialogue

For each Office Action:

1. Verify every legal citation, reference identity, publication/effective date, and
   quoted passage against the primary source.
2. Before drafting amendments or a merits response, independently run the
   prior-art-substance gate below for every 102/103 ground, including every new or
   modified ground. Use `assets/prior-art-validation.md` and preserve it in the
   prosecution record.
3. Put every ground and formal issue in a stable issue ledger. Track affected claims,
   evidence, response, amendment, support location, examiner disposition, and the
   outer agent's separate validation status.
4. Draft an applicant response in the supplied template. Address every rejection and
   objection distinctly, state whether it is traversed or cured, and respond
   claim-by-claim. Preserve alternative arguments when useful.
5. For each proposed amendment, provide exact marked-up language, a clean claim or
   specification replacement, support in the controlling disclosure/evidence,
   scope/commercial impact, and why it resolves the ground.
6. Keep the ground truth unchanged. Build a full proposed candidate and snapshot it.
   Give that exact candidate, the response, redline, support map, and updated ledger
   to the same examiner.
7. Ask the examiner to address every argument and amendment, then expressly maintain,
   modify, or withdraw each issue. New grounds require their own complete mapping and
   another response round. Use interview-style clarification where it narrows a real
   disagreement, and memorialize the result.
8. Repeat with the same examiner until it issues `CONDITIONAL_ALLOWABLE`, `ALLOWABLE`,
   or a genuine terminal impasse under the protocol.

### Prior-art-substance gate

The outer agent must sanity-check the substance of every prior-art rejection rather
than accepting the examiner's chart or search snippets. For each ground:

1. Read the complete claim in light of the specification and state the BRI actually
   being tested without importing unclaimed features.
2. Read the full relied-on reference and the cited passage in its surrounding
   disclosure. Trace figures, reference numerals, cross-references, and the relied-on
   embodiment. Distinguish an operative teaching from background discussion, a
   problem statement, an abandoned or criticized approach, a prophetic possibility,
   or a different alternative embodiment.
3. Reconstruct the claimed arrangement or process and the reference's arrangement or
   process in plain technical terms. For every limitation, record the exact cite,
   what the passage teaches in context, and whether the mapping is `express`,
   `inherent`, `proposed 103 modification`, or `POSITA knowledge/evidence`. Similar
   words, goals, or outputs alone do not establish the required structure, steps,
   relationships, conditions, or sequence. Conversely, do not demand the same label,
   purpose, or implementation detail when the claim does not require it.
4. For anticipation, verify that one enabled reference discloses the limitations in
   the claimed arrangement; do not assemble the claim from unrelated alternatives.
   For obviousness, identify the base embodiment, each actual difference, the exact
   modification or combination, the reason to make it, compatibility and reasonable
   expectation of success, and how the resulting system meets the whole claim.
5. Assign an outer validation status: `prima-facie-supported`, `challenge-pending`,
   or `cannot-assess`. Keep this separate from the examiner's `maintained`,
   `modified`, or `withdrawn` disposition. An unsupported status is available only
   after the reconsideration exchange below.

If the audit reveals a material mismatch, omission, ambiguous passage, or
embodiment-stitching concern, do not yet label the rejection unsupported. Send a
focused `PRIOR_ART_ACCURACY_CHALLENGE` from the validation template to the same
examiner before proposing any curative amendment. Quote the exact claim language,
identify the cited and conflicting context, explain the suspected error neutrally,
and ask the examiner to reread the full reference and either:

- `CONCUR_AND_WITHDRAW` with the error identified;
- `CORRECT_OR_MODIFY` with a complete corrected mapping and ground; or
- `MAINTAIN_WITH_SUPPORT` with the construction, contextual disclosure, and reasoning
  that answer the concern.

Independently evaluate that response. Examiner agreement is useful but not
dispositive. If the examiner concurs and withdraws, mark the outer status
`unsupported-examiner-concurred-and-withdrew`. If it corrects or modifies the ground,
mark the original validation `superseded-by-modified-ground`; treat materially new
passages, references, claim constructions, or combination rationales as a modified or
new ground that receives a fresh gate and a full opportunity to respond. If the
examiner maintains a ground but still cannot support the disputed mapping, mark the
outer status `unsupported-on-current-record-examiner-maintained`, traverse without
narrowing, and keep the examiner issue outstanding. Do not represent an outer-agent
disagreement as examiner withdrawal or allowance. Withdrawal of one ground is not a
clearance unless the complete search, claim, issue, and formal-matter requirements
for clearance are independently satisfied.

If the first reply does not address the focused concern, send one follow-up that
identifies the omitted question. If the examiner again ignores it, relies on the same
demonstrably mismatched passage without analysis, or silently changes theories, close
that cycle as `examiner-protocol-failure` with zero clearance credit and start a new
fresh cycle. Do not use protocol failure merely for a reasonable claim-construction
or technical dispute; those remain in the ordinary dialogue.

Do not pressure the examiner to agree, reveal a target number of clearances, or cite
token/time pressure. Persuasion must rest on the record, law, evidence, and exact
claim language.

For a pending application, every amendment must have support in the application as
filed and must not introduce new matter. For a pre-filing draft, additions may be
made only from authentic inventor-supplied technical facts or evidence; label them
for inventor confirmation and never fabricate disclosure merely to cure a rejection.

## Phase 3 - Close and promote a cleared cycle

The current examiner may issue `CONDITIONAL_ALLOWABLE` only when all ledger items are
resolved and the exact proposed candidate would be in condition for allowance. Its
notice must identify the candidate hash, all pending claim statuses, the dispositive
amendments/arguments, reasons for allowability, closest art, search scope, and any
residual uncertainty. Formal matters still outstanding prevent clearance.

Before crediting that notice, confirm that every prior-art ground considered during
the cycle has a completed validation record, every focused accuracy challenge has an
examiner disposition and outer post-reconsideration determination, and no material
`cannot-assess` item remains. An examiner clearance does not override an incomplete
outer validation gate.

Only after that notice:

1. Apply the accepted candidate verbatim to the ground truth.
2. Re-render and inspect the entire application, not only changed pages.
3. Re-run deterministic parsing/mechanical checks affected by the amendments.
4. Run `cycle_state.py promote` against the ground-truth files. A hash mismatch voids
   the clearance until the same examiner reviews the actual applied version.
5. Preserve the Office Action, every response, redlines, clean candidate, reference
   set, search log, ledger, and notice in the cycle folder.

## Phase 4 - Repeat with fresh examiners

After promotion, spawn a different fresh-context examiner and repeat Phases 1-3. The
new examiner receives the current ground truth and evidence packet, but not earlier
examiner reasoning, applicant dialogue, allowance rationale, or clearance count.
Prior art and public prosecution materials may be included as raw evidence.

A clearance belongs only to the exact promoted version it examined. If any later
examiner causes a substantive application change, the new version starts with zero
qualifying clearances. Continue until two distinct fresh examiners independently
clear the same promoted version. An examiner may clear it without amendments; record
that as `ALLOWABLE` on the already-promoted version.

## Termination conditions

Terminate successfully only when `cycle_state.py status` reports at least two
distinct qualifying examiner IDs for the current promoted version and all of these
are true:

- both examiners received complete enough packets and performed documented searches;
- every pending claim and every issue has an explicit disposition;
- every 102/103 ground, including each modified ground, has a completed substance-
  validation record with no `challenge-pending` or material `cannot-assess` status;
- no rejection, objection, restriction/election requirement, or formal requirement
  remains outstanding;
- both decisions identify the same application-content hash;
- no application-content change occurred after either qualifying clearance.

Terminate as blocked, without claiming success, when essential confidential or
external evidence remains unavailable; reliable prior-art or legal-source access is
impossible; the only cure would add unsupported new matter; no supported amendment
can preserve a user-required objective; a statutory/priority defect is not curable by
drafting; or a necessary inventor/applicant decision is missing. Exhaust reasonable
in-scope research and narrower supported alternatives first. An arbitrary round cap,
budget pressure, examiner fatigue, or repeated disagreement is not a success
condition.

## Final deliverables

Return:

- the final ground-truth application in its original editable format plus a clean
  rendered review copy;
- a version history with hashes and the exact two qualifying examiner context IDs;
- each simulated Office Action, applicant response, interview summary, issue ledger,
  prior-art validation record and accuracy-challenge exchange, amendment redline,
  search log, and allowance notice;
- a concise change/support/scope-impact table;
- unresolved `cannot assess` items and residual risks, including search limitations;
- a prominent statement that this was an AI simulation, not legal advice, an actual
  USPTO examination, or assurance of allowance, validity, or enforceability.

Do not file the application, submit an Office Action response, contact the USPTO, or
make inventor declarations without the user's separate explicit authorization.
