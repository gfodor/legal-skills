---
name: patent-workaround
description: Adversarially pressure-test a draft or pending U.S. utility patent against technically credible, commercially plausible design-arounds that preserve its value proposition while avoiding the current proposed claims. Use fresh competitor subagents, then have the outer agent decide whether each workaround remains inside the invention's intended umbrella based on the design objectives, motivating problem, disclosed solution, and any deployed implementation; strengthen supported claims or disclosure only after new-matter, written-description, enablement, prior-art, eligibility, definiteness, and prosecution-risk gates. Use for design-around testing, workaround resistance, claim-scope gap analysis, competitive-evasion review, or iterative patent-scope hardening; not as an infringement opinion, freedom-to-operate opinion, patentability guarantee, or substitute for patent counsel.
---

# Adversarial patent workaround testing

Run a version-locked competitor/drafter loop. Keep the main agent in the strategic
patent-drafter role and use a fresh subagent as the competitor/product architect for
each challenge cycle. The goal is not maximal claim breadth. The goal is supported,
patentable coverage of commercially material alternatives that genuinely belong to
the invention, with deliberate visibility into what remains outside the claims.

Never describe a result as proof of infringement, noninfringement, validity,
enforceability, patentability, or freedom to operate. Recommend review by qualified
patent counsel before filing or relying on any amendment.

## Read before acting

Read all of these files completely:

- `references/workaround-protocol.md` for the adversary's role and output contract.
- `references/integration-gates.md` for umbrella classification and amendment gates.
- `references/current-sources.md` for the current-law and prior-art source hierarchy.

Copy and complete `assets/workaround-intake.yaml`,
`assets/invention-thesis.md`, `assets/search-record.md`, and
`assets/evidence-manifest.json`. Use `assets/adversary-handoff.md` and a completed
`assets/adversary-brief.md` for every fresh subagent, maintain
`assets/coverage-ledger.md` throughout the run, and copy
`assets/outer-adjudication.md` for every outer-agent disposition.

If the sibling `../patent-audit` skill is installed, read its `SKILL.md` and use its
parser and deterministic pre-pass to obtain the claim dependency graph, element
decomposition, section inventory, and mechanical findings. If `../patent-examine`
is installed, use its current-law, prior-art, and prosecution-risk discipline when
testing a proposed claim package. A prior audit or examination does not substitute
for this workaround loop.

## Non-negotiable distinctions

Maintain all of these distinctions in every report:

1. **Claim coverage** asks whether every limitation of at least one relevant claim
   is met. It is a legal-scope hypothesis, not an umbrella judgment.
2. **Workaround credibility** asks whether the alternative can plausibly deliver
   materially the same user or commercial value. A toy omission that destroys the
   value is not a meaningful workaround.
3. **Umbrella alignment** asks whether the credible alternative belongs in the
   intended patent-family or filing thesis in view of the motivating problem, design
   objectives, deployed solution, commercial substitution, and user-defined scope.
   It is strategic: an alternative may be umbrella-aligned even when the current
   application does not support it. It does not expand the legal scope of the claims.
4. **Disclosure support** asks what the authoritative application actually teaches
   or reasonably conveys. Business intent, a broad value proposition, or a newly
   imagined alternative is not automatically written-description support.
5. **Patentability** asks whether a proposed capture strategy survives current-law
   and prior-art scrutiny. A workaround can expose a real commercial gap that cannot
   safely be claimed.

Do not say a workaround is "covered by the patent" merely because it falls under the
invention's theme. Narrative language can support construction or future claims,
but exclusionary scope comes from claims and applicable law.

## State and evidence model

Create a dedicated run directory and preserve the user's original files. Maintain:

1. **Ground truth**: the authoritative editable application, frozen during a cycle.
2. **Challenge candidate**: a complete clean application with the exact proposed
   claims and disclosure for the next adversary.
3. **Frozen challenge packet**: the candidate plus every decision-controlling input,
   including intake, invention-thesis map, prosecution history, deployed-product
   facts, search record, and an evidence manifest containing hashes for raw evidence.
4. **Challenge record**: adversary reports, claim
   charts, support maps, prior-art search records, coverage ledger, redlines,
   decisions, version hashes, and unresolved risks.

Use `scripts/coverage_state.py` to lock challenge packets and independent decisions.
A fresh decision applies only to the explicit version and packet hash it reviewed.
Any material change to the application, invention thesis, prosecution record,
deployed-product facts, search evidence, or other decision input requires a new
packet version and resets qualifying challenge decisions.

```powershell
python scripts/coverage_state.py init --run-dir workaround_run `
  --candidate application=application.docx --candidate drawings=drawings.pdf `
  --candidate intake=intake.yaml --candidate thesis=invention-thesis.md `
  --candidate search=search-record.md --candidate evidence=evidence-bundle.zip `
  --authoritative application --authoritative drawings

python scripts/coverage_state.py snapshot --run-dir workaround_run `
  --candidate application=proposal/application.docx `
  --candidate drawings=proposal/drawings.pdf --candidate intake=intake.yaml `
  --candidate thesis=invention-thesis.md --candidate search=search-record.md `
  --candidate evidence=evidence-bundle.zip

$packetHash = "<copy packet_sha256 from snapshot output>"

python scripts/coverage_state.py record --run-dir workaround_run `
  --version v002 --packet-sha256 $packetHash --adversary competitor-01 `
  --stage raw --decision gaps-found `
  --document workaround_run/competitor-01/report.md

python scripts/coverage_state.py record --run-dir workaround_run `
  --version v002 --packet-sha256 $packetHash --adversary competitor-01 `
  --stage adjudication --decision only-accepted-gaps `
  --document workaround_run/competitor-01/adjudication.md `
  --ledger workaround_run/coverage-ledger.md

# Repeat with a second fresh adversary. After two qualifying dispositions, apply the
# proposal verbatim and verify the complete challenged packet:
python scripts/coverage_state.py promote --run-dir workaround_run `
  --version v002 --candidate application=application.docx `
  --candidate drawings=drawings.pdf --candidate intake=intake.yaml `
  --candidate thesis=invention-thesis.md --candidate search=search-record.md `
  --candidate evidence=evidence-bundle.zip

python scripts/coverage_state.py status --run-dir workaround_run
```

Use stable labels for all packet components. `application`, `intake`, `thesis`,
`search`, and `evidence` are required; `drawings` is optional at initialization but
cannot later be silently added or omitted. Every label passed with `--authoritative`
is an authoritative editable destination. Mark `application` and every separately
supplied specification, claims, abstract, drawing, sequence, or appendix source as
authoritative. Promotion succeeds only after the accepted bytes have been applied to
all of those exact paths. Later status checks fail if a promoted authoritative file
drifts from the promoted packet.

Run `coverage_state.py` commands serially from one outer agent. The state writer is
not a multi-process transaction service; do not issue parallel record or snapshot
commands.

Use the relevant document and PDF skills to preserve source formatting, claim
numbering, dependencies, tracked changes, equations, and drawings. Never edit an
extraction and present it as the authoritative source.

## Phase 0 - Intake and completeness gate

Obtain or locate:

- the complete specification, claims, abstract, drawings, appendices, and editable
  source;
- application status, filing and priority facts, public-disclosure facts, and the
  complete prosecution history if filed;
- the intended value proposition, target users, motivating problem, design
  objectives and constraints, asserted inventive mechanisms, and indispensable
  commercial coverage;
- the actual deployed or prototyped solution, including actors, boundaries, data or
  material flow, control locus, timing, optional features, and known substitutes;
- closest prior art, search logs, related patents/applications, cited references,
  known competitor approaches, and relevant technical evidence;
- inventor-confirmed alternatives and generalizations already contemplated.

Do not infer missing inventor facts. Mark them `missing` and distinguish `cannot
assess` from `no gap found`. If readable claims or enough disclosure to construe them
is missing, return `INCOMPLETE` rather than inventing a workaround test.

Before sending confidential unpublished details to public search services, explain
the exposure and obtain authorization. Search public abstractions or local materials
when that can answer the question without disclosing confidential subject matter.

## Phase 1 - Build the invention-thesis map

Build an evidence-cited map with separate rows for:

- customer or operational outcome and value proposition;
- motivating problem and shortcomings of prior approaches;
- design objectives, constraints, and tradeoffs;
- the disclosed inventive mechanism or mechanisms;
- the deployed or prototyped implementation, if any;
- required versus optional features and actor/system boundaries;
- supported alternatives, substitutions, generalizations, and claim classes;
- non-negotiable business scope and acceptable deliberate gaps;
- disclaimers, definitions, prior-art characterizations, amendments, arguments, and
  other possible scope surrender.

For every row, identify the source and exact location, distinguish inventor-supplied
fact from drafter inference, and assign `confirmed`, `inferred`, `disputed`, or
`missing`. Do not collapse an aspirational objective into a disclosed invention.

Refresh the legal-source record and run or update a documented prior-art search.
Search both the existing claims and the generalized inventive concepts likely to be
used to capture alternatives. Preserve queries, databases, dates, classifications,
full references, and pin cites. Use discovery sources to find art, then verify the
actual primary references.

Create a deterministic evidence bundle containing the completed evidence manifest
and every supplied prosecution, product, prior-art, and technical-evidence file.
Sort entries, use stable internal paths and timestamps, and rebuild it whenever
decision-controlling evidence changes. Use that one bundle as the required
`evidence` packet component in every `init`, `snapshot`, and `promote` call. Changing
its bytes creates a new version without changing the packet-label schema. Exclude
the bundle and manifest from the manifest's own raw-evidence list; the state tool
records the bundle's actual hash.

## Phase 2 - Dispatch one fresh adversary

Create a unique context ID such as `competitor-01`. Spawn a fresh subagent that has
not seen prior workaround reports, outer-agent proposed fixes, accepted gaps, or the
desired answer. Provide only:

- the frozen candidate and version/hash;
- the completed handoff and adversary-safe factual/value brief;
- viewable drawings and relevant deployed-product facts;
- the current claim set and prosecution history needed to assess scope;
- public prior art and technical evidence needed for credible engineering.

Use the actual canonical spawned-agent or session identifier as the adversary context
ID and preserve the spawn/handoff record. The state tool verifies distinct asserted
IDs and report bytes, but cannot authenticate subagent freshness without that
orchestrator provenance.

Do not give the adversary the full intake, full invention-thesis map, coverage
ledger, accepted deliberate gaps, acceptable or unacceptable narrowing, desired
claim classes, counsel decisions, or applicant capture strategy. Build
`assets/adversary-brief.md` only from frozen packet evidence and remove those fields
before dispatch. The outer agent retains the unredacted materials for adjudication.

Tell the subagent not to inspect other adversaries' folders. Give it
`references/workaround-protocol.md` as its controlling contract. It must preserve the
value proposition, systematically mutate claim limitations and system boundaries,
and return technically specific alternatives with claim-by-claim avoidance maps.
Require its UTF-8 text report to carry the exact context ID, version, packet hash,
and decision headers from that protocol; the state tool rejects inconsistent
metadata.

Do not disclose a target outcome, target number of cycles, or amendments the outer
agent hopes to make. Do not reward superficial novelty: alternatives that merely
remove the value, depend on impossible engineering, or rename a claimed element are
not successful workarounds.

## Phase 3 - Outer-agent adjudication

Independently verify every proposed workaround using `integration-gates.md` and the
coverage ledger. Do not accept the adversary's infringement or umbrella conclusion.
For each workaround:

1. Verify technical feasibility and whether the material value proposition remains.
2. Chart every limitation of every relevant independent claim. Identify the exact
   limitation allegedly absent or materially changed, and test other claim classes,
   actor combinations, direct infringement theories, and applicable equivalents
   risk separately. Do not use the doctrine of equivalents as a substitute for clear
   claim drafting.
3. Classify the workaround as `not-a-workaround`, `outside-umbrella`,
   `umbrella-gap-supported`, `umbrella-gap-unsupported`, or `cannot-assess`.
4. Cite the objectives, problem, solution mechanism, disclosure, deployed facts, and
   user-defined business scope supporting that classification. A label without an
   evidence trail is not a disposition.
5. For a material umbrella gap, identify the narrowest capture strategy that covers
   the alternative without unnecessarily claiming the result itself.
6. Apply every support, patentability, prosecution-history, and scope-quality gate
   before recommending or drafting a change.

Do not classify an alternative `outside-umbrella` merely because it is absent from
the disclosure, uses a new technical mechanism, or conflicts with present claim
language. Decide strategic alignment first; use `umbrella-gap-unsupported` when an
aligned alternative lacks filing-date support.

Challenge false positives first. A workaround that actually meets another
independent claim, sacrifices indispensable value, or merely exploits an implausible
construction is not evidence that the application must change.

## Phase 4 - Integrate only safe, supported changes

Use this order of preference, stopping at the first defensible remedy:

1. Correct a genuine construction or consistency defect.
2. Revise or add a supported independent claim directed to the inventive mechanism
   at the appropriate level, including parallel method, system, device, composition,
   or computer-readable-medium classes when justified.
3. Add supported dependent fallbacks that preserve narrower patentable positions.
4. Improve the summary or detailed description with supported objectives,
   mechanisms, embodiments, alternatives, and boundary variations.
5. Recommend a continuation, divisional, continuation-in-part, reissue, or separate
   filing for counsel assessment when status and law permit; do not assume priority,
   inventorship, or entitlement.
6. Record a deliberate gap when capture would add unsupported matter, collide with
   prior art, create unacceptable rejection/validity risk, or exceed the invention.

For a pending application, map every claim or disclosure amendment to the
application as filed and prohibit new matter. For a pre-filing draft, add technical
content only from authentic inventor-supplied facts or evidence, label it for
inventor confirmation, and never fabricate embodiments. Treat an issued patent as a
different procedural posture; do not rewrite it as though it were still a draft.

For each proposed claim change, conduct a targeted search and analyze at least
35 U.S.C. 101, 102, 103, 112(a), 112(b), and 112(f) where applicable, plus
restriction, double-patenting, claim-class, priority, inventorship, and prosecution-
history consequences. Prefer a narrower supported claim family over an unsupported
genus or result-only claim. Preserve exact support citations and explain commercial
scope gained and fallback scope lost.

For a pending application, route potentially material information discovered in
search or adversarial review to qualified counsel or another authorized person and
track materiality/IDS/timing triage in the search record and ledger. Do not make the
ultimate disclosure decision or file an IDS. Unresolved potentially material
information awaiting authorized review blocks promotion.

For narrative changes, state their limited legal purpose. Avoid admissions about
what the prior art lacks or teaches, unnecessary definitions, mandatory language,
categorical statements, disparagement, disclaimer, and disclosure of an alternative
without a considered claiming strategy. Narrative alone does not close a claim gap.

Keep ground truth unchanged while preparing a complete clean challenge candidate,
redline, claim charts, support map, search update, and revised ledger. Snapshot that
exact candidate and all changed decision inputs before the next challenge.

## Phase 5 - Repeat on the exact candidate

Dispatch a different fresh-context adversary against the exact current challenge
candidate and repeat Phases 2-4. The new adversary receives that complete candidate
and raw evidence, but no prior adversary reasoning, outer-agent fix rationale, or
qualifying decision count. Keep an amended candidate unpromoted while it is being
challenged; an unchanged initial ground truth may already be marked promoted.

A cycle receives a qualifying outer-agent disposition only after the raw adversary
report and every resulting ledger row have been independently adjudicated:

- `no-material-gap`: the adversary returned `NO_MATERIAL_GAP`, and the outer agent
  verified that the required attack matrix and evidence support that result; or
- `only-accepted-gaps`: the adversary returned `GAPS_FOUND`, but outer adjudication
  showed every candidate was not a workaround, outside the umbrella, or a supported
  deliberate gap expressly accepted by the user and counsel for a documented
  business reason. An `umbrella-gap-unsupported` candidate never qualifies under
  this disposition.

Record the raw decision first, then record the qualifying outer disposition against
the same adversary ID with an adjudication document. Pass the explicit reviewed
version and packet hash to both record commands. The state tool accepts only
`NO_MATERIAL_GAP` → `no-material-gap` and `GAPS_FOUND` → `only-accepted-gaps` as
qualifying raw/adjudication pairs. Require qualifying dispositions for two distinct
fresh adversaries on the same packet. Only then apply an amended candidate verbatim
to ground truth and run `coverage_state.py promote`; the tool rejects both early
promotion and a packet-hash mismatch. A later material input change resets the
count. This is an exhaustion rule for the workflow, not proof that no competitor
can design around the claims.

Complete `assets/outer-adjudication.md` from the coverage ledger and save it as UTF-8
text. The state tool validates the adversary context ID, version, packet hash, and
outer disposition in both decision documents against the command arguments. It also
binds the adjudication to the latest raw-report hash and supplied archived
coverage-ledger hash and requires every gate confirmation to be `YES`. Never reuse
one raw report under a second adversary ID or reuse an adjudication after a new raw
report.

Do not turn a productive adversary into a drafter. The outer agent owns umbrella
classification, legal-risk verification, and amendments; the adversary owns the
attack.

## Termination conditions

Terminate successfully only when `coverage_state.py status` reports two qualifying
fresh adversaries for the current promoted version and all material workaround rows
have an evidence-cited disposition, support result, prior-art result, and capture or
acceptance decision.

Terminate as blocked, without claiming robust coverage, when essential application,
prosecution, product, inventor, or priority facts remain unavailable; public search
would expose confidential material and authorization is withheld; the only capture
strategy requires unsupported new matter; reliable prior-art or current-law research
is unavailable; or a required inventor/applicant/counsel business choice is missing.
Any material `umbrella-gap-unsupported` candidate is blocking even if the user is
willing to tolerate it; record that risk, but do not issue a qualifying disposition.
Exhaust reasonable narrower supported alternatives first. An arbitrary round cap,
token pressure, or adversary fatigue is not success.

## Final deliverables

Return:

- the final editable ground truth plus a clean rendered review copy and redline;
- the invention-thesis map and version history with packet hashes;
- every adversary handoff/report and the exact two qualifying context IDs;
- the coverage ledger with claim charts, umbrella classification, support, prior-art
  and risk dispositions for every workaround;
- a claim amendment package with clean/marked claims and exact support citations;
- a narrative amendment package distinguishing capture-support edits from context;
- search logs, verified references, residual risks, accepted gaps, and items that
  remain `cannot-assess`;
- a concise statement of coverage gained, scope or fallback positions lost, and
  business consequences;
- a prominent statement that the work was an AI-assisted pressure test, not legal
  advice, an infringement or freedom-to-operate opinion, or assurance of validity,
  enforceability, patentability, allowance, or competitor behavior.

Do not file, submit amendments, contact the USPTO, contact competitors, or make
inventor declarations without the user's separate explicit authorization.
