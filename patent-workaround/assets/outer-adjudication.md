OUTER_DISPOSITION: REPLACE_WITH_A_VALID_DISPOSITION
ADVERSARY_CONTEXT_ID: REPLACE_WITH_CONTEXT_ID
APPLICATION_VERSION_ID: REPLACE_WITH_VERSION_ID
APPLICATION_PACKET_SHA256: REPLACE_WITH_PACKET_SHA256
RAW_REPORT_SHA256: REPLACE_WITH_RAW_REPORT_SHA256
COVERAGE_LEDGER_SHA256: REPLACE_WITH_COVERAGE_LEDGER_SHA256
GATE_LEDGER_COMPLETE: NO
GATE_SUPPORT_COMPLETE: NO
GATE_PRIOR_ART_COMPLETE: NO
GATE_CAPTURE_DECISIONS_COMPLETE: NO
GATE_NO_UNRESOLVED_MATERIAL_ITEMS: NO
GATE_NO_UNSUPPORTED_UMBRELLA_GAPS: NO

# Outer-agent workaround adjudication

Replace `OUTER_DISPOSITION` with exactly one of:

- `NO_MATERIAL_GAP` after independently verifying a raw `NO_MATERIAL_GAP` report;
- `ONLY_ACCEPTED_GAPS` after adjudicating every candidate in a raw `GAPS_FOUND`
  report; or
- `BLOCKED` or `WITHDRAWN` when the cycle does not qualify.

Replace every header value. A qualifying disposition requires all six gate headers
to say exactly `YES`. Use `BLOCKED`, not `ONLY_ACCEPTED_GAPS`, whenever any material
candidate is `umbrella-gap-unsupported`.

## Raw report binding

- Raw report path and SHA-256:
- Raw decision:
- Coverage-ledger path and SHA-256:

## Candidate dispositions

| Workaround ID | Claim result | Umbrella classification | Support result | Prior-art result / search IDs | Capture or acceptance decision |
|---|---|---|---|---|---|

## Gate confirmation

- Every material candidate has an evidence-cited disposition:
- Every material candidate has a support and enablement result:
- Every material candidate has a verified prior-art result or `cannot-assess`:
- Every gap has a capture decision or authorized acceptance record:
- No unresolved material ledger row is being treated as favorable:

## Rationale and residual limits

State why the disposition follows from the exact packet. Do not claim infringement,
noninfringement, validity, enforceability, patentability, or freedom to operate.
