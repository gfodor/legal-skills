# Office Action and applicant-response rules

## Simulated Office Action structure

Use numbered paragraphs and this order when applicable:

1. **Simulation header**: application identifier, version/hash, examination date,
   effective filing/priority assumptions, AIA/pre-AIA framework, and decision.
2. **Application status**: every pending claim and its status; amendments considered;
   elected invention/species; attachments and reference list.
3. **Search record**: databases, queries, synonyms, CPC/USPC classes, date limits,
   citation chaining, non-patent literature, search date, and limitations.
4. **Claim interpretation**: material broadest-reasonable-interpretation findings and
   any 35 U.S.C. 112(f) treatment.
5. **Restrictions, objections, and requirements**: keep these distinct from claim
   rejections and state how each can be traversed or cured.
6. **Grounds of rejection**: group claims only when the same analysis genuinely
   applies. Assign a stable issue ID and identify each rejected claim. For prior-art
   grounds, include a reference-substance synopsis and contextual limitation chart.
7. **Allowable subject matter**: identify claims or specific subject matter that
   would be allowable if rewritten, without treating it as a clearance of the whole
   application.
8. **Response instructions**: enumerate every issue requiring a response.
9. **Issue ledger**: one row per issue with affected claims and current status.

## Minimum support by ground

### Prior-art mapping fields

For every 102/103 reference, summarize the operative technical disclosure, relied-on
embodiment, figures/reference numerals, and relevant material, data, control, or step
flow. Do not use an abstract, search snippet, or isolated passage as a substitute for
the full disclosure.

Each limitation-chart row must include:

- the exact claim language and material BRI;
- the reference, specific embodiment, and exact contextual pin cites;
- what the cited disclosure affirmatively teaches in that context;
- the mapping mode: `express`, `inherent`, `proposed 103 modification`, or
  `POSITA knowledge/evidence`;
- how the required structure, relationship, condition, or sequence is met; and
- any material alternative-embodiment, incompatibility, or counterteaching issue and
  why it does or does not change the mapping.

A lexical or high-level functional similarity is not a substitute for the technical
mapping. Do not require an unclaimed label, purpose, or implementation detail.

### 35 U.S.C. 101

Analyze each affected claim, not merely the specification's theme. Identify the
statutory category and utility issue, if any. For eligibility, apply the current
USPTO Step 2A/Step 2B procedure and current controlling precedent. Identify the exact
judicial exception, additional elements, practical-application analysis, and any
well-understood/routine/conventional finding with the required factual support. Do
not cite guidance itself as the substantive legal basis for rejection.

### 35 U.S.C. 102

Identify the precise statutory subsection and why the reference qualifies as prior
art for the claim's effective filing date. One enabled reference must disclose every
limitation, expressly or inherently, arranged as claimed under the BRI. Provide a
claim chart with one row per limitation and contextual pin cites. Show why limitations
drawn from different passages belong to one disclosed arrangement rather than
unrelated embodiments or selections. For inherency, show necessity rather than a
mere possibility. Additional references may only perform a legally permitted
explanatory role; do not disguise a multi-reference obviousness theory as
anticipation. Criticism or teaching away does not erase an otherwise enabled
anticipatory disclosure, but a goal or unsupported possibility is not enough.

### 35 U.S.C. 103

Identify the statutory framework and all references. State findings on the scope and
content of the prior art, differences from each claim, and the pertinent skill level.
Identify the base embodiment and map every limitation with contextual pin cites.
State candidly which limitations the unmodified base lacks. Articulate the exact
modification or combination, a reason a skilled artisan would have made it at the
relevant time, compatibility and reasonable expectation of success, and how the
resulting arrangement meets the whole claim. Do not conflate separate embodiments or
write the proposed modification back into the reference as an existing teaching.
Address analogous art, the references as a whole, teaching away, incompatibility,
hindsight, and timely objective evidence when raised. “Common sense,” design choice,
optimization, and official notice require facts and reasoning, not labels.

### 35 U.S.C. 112(a)

Separate written description, enablement, and best-mode theories. Identify the exact
claim scope lacking possession or enablement and the disclosure relied on. For
enablement, explain why the necessary experimentation would be undue in view of the
full claim scope and relevant Wands considerations; do not demand working examples as
an automatic rule. Treat new-matter concerns as distinct from whether an amendment
has as-filed support.

### 35 U.S.C. 112(b) and 112(f)

Identify the exact word, phrase, relationship, or claim boundary that is unclear and
why a skilled artisan cannot determine the scope with reasonable certainty under the
BRI. Do not reject merely because language is broad. Address antecedent basis,
inconsistent terminology, functional language, relative terms, mixed statutory
classes, and improper dependencies only when they create a real statutory defect.
For 112(f), identify the claimed function and corresponding disclosed structure,
material, or acts; for computer-implemented functions, assess the disclosed
algorithm where current law requires one.

### Other grounds and formal matters

Address double patenting, restriction/election, inventorship, priority/benefit,
drawings, sequence listings, claim form, specification objections, and information
requirements only when the packet supports them. Distinguish rejection from
objection and requirement. Do not simulate a terminal disclaimer, declaration, or
inventor factual statement.

## Applicant response structure

Mirror real prosecution while keeping the ground truth unchanged:

1. identify the Office Action, application version/hash, response round, and every
   issue being answered;
2. provide a claim-status table and exact marked-up amendments;
3. provide clean replacement claims/specification text;
4. for a pending case, map every added or altered feature to as-filed support,
   including drawing support; for a pre-filing draft, identify the authentic
   inventor-supplied fact/evidence supporting every new disclosure;
5. separately traverse or cure every rejection, objection, and requirement;
6. respond to the examiner's claim construction before applying prior art;
7. explain technical errors with primary evidence and declarations/test data only
   when authentic and authorized;
8. state scope and commercial impact, including deliberate surrender and preserved
   alternatives;
9. include an updated issue ledger with separate examiner-disposition and outer-
   validation fields, the completed prior-art validation records, and a full clean
   proposed candidate.

Arguments must match the claim language. Avoid accidental admissions, categorical
statements about the prior art, unnecessary definitions, and assertions broader than
the evidence. Do not amend a claim to overcome an unsupported rejection before first
testing the rejection's prima facie sufficiency.

## Disposition test

After every response, the examiner must give a reasoned disposition for every issue.
The response is incomplete until the union of the claim-status table and issue ledger
accounts for all pending claims, all earlier grounds, all new grounds, and all formal
matters. Only an empty outstanding-issue set permits allowability.
