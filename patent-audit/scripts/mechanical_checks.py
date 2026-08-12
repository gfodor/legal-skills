#!/usr/bin/env python3
"""Deterministic checks over parsed.json — the checks a model should never run.

Models are unreliable at exhaustive cross-referencing (they find 19 of 20
numerals and report "all consistent") and at arithmetic. Those checks belong
here, where they are exact. Everything requiring judgment is left to the agents.

    python mechanical_checks.py parsed.json [-o findings_mechanical.json]
                                [--intake intake.yaml]

Each check emits a finding in the shared schema:
    {item_id, verdict, severity, location, evidence, explanation, suggested_fix,
     source: "mechanical"}

verdict is one of: pass | fail | cannot_assess | not_applicable
A check that lacks its input emits `cannot_assess`, never `pass`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Checks that narrow a search but cannot decide it emit `cannot_assess` with a
# populated `candidates` field for the owning agent to adjudicate.
CHECKS = []


def check(item_id, severity, title, covers=()):
    """Register a check.

    `covers` lists the checklist item IDs this check contributes a verdict to.
    A contribution is not necessarily the whole item: synthesize.py keeps the
    worst verdict per item, so a mechanical `pass` never suppresses a later
    `fail` from the agent that owns the judgment half of the same item.
    """
    def deco(fn):
        CHECKS.append((item_id, severity, title, tuple(covers), fn))
        return fn
    return deco


def finding(item_id, severity, verdict, explanation, location="", evidence="",
            fix="", candidates=None):
    f = {"item_id": item_id, "verdict": verdict, "severity": severity,
         "location": location, "evidence": evidence, "explanation": explanation,
         "suggested_fix": fix, "source": "mechanical"}
    if candidates is not None:
        f["candidates"] = candidates
    return f


# ------------------------------------------------------------------ claim form

@check("G_DEP_GRAPH", "Fatal", "Claim dependency graph is valid",
       covers=["G04", "G53"])
def dependency_graph(p, intake):
    claims = p["claims"]
    if not claims:
        return finding("G_DEP_GRAPH", "Fatal", "cannot_assess",
                       "No claims were parsed from the draft.")
    bad = []
    for c in claims:
        if c["dangling_parents"]:
            bad.append("claim %d depends on non-existent claim(s) %s"
                       % (c["number"], c["dangling_parents"]))
        if c["forward_reference"]:
            bad.append("claim %d refers to claim %s, which does not precede it"
                       % (c["number"], c["forward_reference"]))
    nums = [c["number"] for c in claims]
    if nums != list(range(1, len(nums) + 1)):
        bad.append("claims are not numbered consecutively from 1: %s" % nums)
    if not any(c["type"] == "independent" for c in claims):
        bad.append("no independent claim found")
    if bad:
        return finding("G_DEP_GRAPH", "Fatal", "fail", "; ".join(bad),
                       location="claims",
                       fix="Renumber and repoint claim dependencies so every "
                           "dependent claim refers back to an earlier claim.")
    return finding("G_DEP_GRAPH", "Fatal", "pass",
                   "%d claims, all dependencies resolve to earlier claims, "
                   "numbering consecutive." % len(claims))


@check("G_ONE_SENTENCE", "Serious", "Each claim is a single sentence",
       covers=["G06", "G47"])
def one_sentence(p, intake):
    bad = [c for c in p["claims"] if c["internal_periods"] > 0]
    if not p["claims"]:
        return finding("G_ONE_SENTENCE", "Serious", "cannot_assess", "No claims parsed.")
    if bad:
        return finding(
            "G_ONE_SENTENCE", "Serious", "fail",
            "Claims with a sentence-ending period mid-claim: %s"
            % ", ".join(str(c["number"]) for c in bad),
            location="claims " + ", ".join(str(c["number"]) for c in bad),
            fix="Recast as a single sentence; use semicolons between elements.")
    return finding("G_ONE_SENTENCE", "Serious", "pass",
                   "All %d claims are single sentences." % len(p["claims"]))


@check("G_CLAIM_PUNCT", "Quality", "Claim punctuation and closing period",
       covers=["G06", "G47"])
def claim_punct(p, intake):
    if not p["claims"]:
        return finding("G_CLAIM_PUNCT", "Quality", "cannot_assess", "No claims parsed.")
    bad = [c["number"] for c in p["claims"] if not c["ends_with_period"]]
    if bad:
        return finding("G_CLAIM_PUNCT", "Quality", "fail",
                       "Claims not terminated by a period: %s" % bad,
                       location="claims %s" % bad,
                       fix="End every claim with a single period.")
    return finding("G_CLAIM_PUNCT", "Quality", "pass", "All claims end with a period.")


@check("G_TRANSITION", "Serious", "Every independent claim has a recognised transition",
       covers=["G46"])
def transitions(p, intake):
    if not p["claims"]:
        return finding("G_TRANSITION", "Serious", "cannot_assess", "No claims parsed.")
    # A dependent claim inherits its parent's transition; only independent
    # claims must carry one of their own.
    missing = [c["number"] for c in p["claims"]
               if not c["transition"] and c["type"] == "independent"]
    closed = [c["number"] for c in p["claims"]
              if c["transition"] in ("consisting_of", "consisting_essentially_of")]
    notes = []
    if closed:
        notes.append("closed transition ('consisting of') narrows scope to the "
                     "recited elements only, in claims %s" % closed)
    if missing:
        return finding("G_TRANSITION", "Serious", "fail",
                       "No transition phrase found in claims %s. %s"
                       % (missing, "; ".join(notes)),
                       location="claims %s" % missing,
                       fix="Insert an explicit transition, normally 'comprising'.")
    return finding("G_TRANSITION", "Serious", "pass",
                   "All claims carry a transition. %s" % ("; ".join(notes) or ""))


@check("G_ANTECEDENT", "Serious", "Antecedent basis candidates",
       covers=["G08", "G09", "G42"])
def antecedents(p, intake):
    cands = []
    for c in p["claims"]:
        for a in c.get("antecedent_candidates", []):
            cands.append({"claim": c["number"], "phrase": a["phrase"], "noun": a["noun"]})
    if not p["claims"]:
        return finding("G_ANTECEDENT", "Serious", "cannot_assess", "No claims parsed.")
    if not cands:
        return finding("G_ANTECEDENT", "Serious", "pass",
                       "No definite reference lacks an earlier indefinite "
                       "introduction in its claim or ancestry.")
    return finding(
        "G_ANTECEDENT", "Serious", "cannot_assess",
        "%d definite references have no earlier antecedent in scope. A model must "
        "adjudicate: an inherent property ('the length of the rod') needs no "
        "antecedent, a missing element does." % len(cands),
        location="claims", candidates=cands,
        fix="For each genuine gap, introduce the element with 'a'/'an' first.")


# Claim language that is structural glue rather than a claimed element. A term
# from this set appearing only in the claims proves nothing.
CLAIM_GLUE = {
    "claim", "claims", "wherein", "comprising", "comprises", "further",
    "according", "consisting", "essentially", "including", "includes", "having",
    "whereby", "means", "said", "configured", "adapted", "thereof", "therein",
    "thereto", "thereon", "respectively", "least", "plurality", "which", "that",
    "being", "generally", "substantially", "approximately", "about", "relatively",
    "disposed", "positioned", "arranged", "coupled", "connected", "attached",
    "mounted", "secured", "provided", "formed", "defined", "extending",
    "operable", "capable", "wherein", "method", "system", "apparatus", "device",
    "assembly", "wherein", "allowing", "causing", "sliding", "moving", "first",
    "second", "third", "fourth", "upper", "lower", "inner", "outer", "material",
}


@check("G_CLAIM_SUPPORT", "Fatal", "Claim terms appear in the specification",
       covers=["G28"])
def claim_support(p, intake):
    """Literal absence of a claim term from the description.

    Deliberately emits `cannot_assess`, not `fail`: a synonym or a described
    genus can support a claim term that never appears verbatim, so only a model
    can tell a real §112 support gap from a wording difference. The script's job
    is to produce an exhaustive candidate list, which it can do exactly.
    """
    spec = " ".join(s.get("text", "") for k, s in p["sections"].items()
                    if k != "claims").lower()
    if not spec.strip():
        return finding("G_CLAIM_SUPPORT", "Fatal", "cannot_assess",
                       "No specification text outside the claims was found.")
    if not p["claims"]:
        return finding("G_CLAIM_SUPPORT", "Fatal", "cannot_assess", "No claims parsed.")
    missing = []
    for c in p["claims"]:
        terms = {t.lower() for t in re.findall(r"\b[a-z][a-z\-]{4,}\b", c["text"], re.I)}
        for t in sorted(terms - CLAIM_GLUE):
            if t not in spec and t.rstrip("s") not in spec:
                missing.append({"claim": c["number"], "term": t})
    if missing:
        return finding(
            "G_CLAIM_SUPPORT", "Fatal", "cannot_assess",
            "%d claim term(s) do not appear verbatim in the description: %s. A "
            "model must decide whether each is genuinely unsupported or merely "
            "worded differently from the specification."
            % (len(missing), ", ".join(sorted({m["term"] for m in missing}))[:400]),
            location="claims", candidates=missing,
            fix="Where support is genuinely absent, add it to the description "
                "before filing — afterwards it is new matter and cannot be added.")
    return finding("G_CLAIM_SUPPORT", "Fatal", "pass",
                   "Every substantive claim term appears verbatim in the description.")


@check("G_MPF", "Serious", "Means-plus-function claims have disclosed structure",
       covers=["G21", "G45"])
def mpf(p, intake):
    mpfs = [c["number"] for c in p["claims"] if c["means_plus_function"]]
    if not mpfs:
        return finding("G_MPF", "Serious", "not_applicable",
                       "No claim uses 'means for' or 'step for'.")
    return finding(
        "G_MPF", "Serious", "cannot_assess",
        "Claims %s invoke means-plus-function treatment. A model must confirm the "
        "specification discloses corresponding structure for each recited function "
        "and links it explicitly." % mpfs,
        location="claims %s" % mpfs, candidates=mpfs,
        fix="For each 'means for X', ensure the spec names the structure that "
            "performs X and ties it to that language.")


# ----------------------------------------------------------- numerals & drawings

@check("H_NUMERAL_XREF", "Serious", "Reference numerals reconcile with the drawings",
       covers=["H03", "F13"])
def numeral_xref(p, intake):
    spec_nums = set(p["reference_numerals"]["numerals"])
    dwg = p.get("drawings")
    if not dwg:
        return finding("H_NUMERAL_XREF", "Serious", "cannot_assess",
                       "No drawings supplied; rerun parse_application.py with "
                       "--drawings to enable this check.")
    if dwg.get("error"):
        return finding("H_NUMERAL_XREF", "Serious", "cannot_assess", dwg["error"])
    sheets = dwg.get("sheets") or []
    if sheets and isinstance(sheets[0], dict):
        dwg_nums = set()
        textless = 0
        for s in sheets:
            dwg_nums |= set(s.get("numerals", []))
            textless += 0 if s.get("has_text_layer") else 1
        if textless == len(sheets):
            return finding("H_NUMERAL_XREF", "Serious", "cannot_assess",
                           "Drawing sheets have no text layer (scanned or vector "
                           "outlines); numerals must be read visually by the "
                           "drawings agent.")
        only_spec = sorted(spec_nums - dwg_nums, key=lambda s: (len(s), s))
        only_dwg = sorted(dwg_nums - spec_nums, key=lambda s: (len(s), s))
        if only_spec or only_dwg:
            return finding(
                "H_NUMERAL_XREF", "Serious", "fail",
                "In specification but not in drawings: %s. In drawings but not "
                "described: %s." % (only_spec or "none", only_dwg or "none"),
                location="drawings",
                candidates={"spec_only": only_spec, "drawing_only": only_dwg},
                fix="Every numeral must appear in both. Add the missing labels or "
                    "delete the orphaned ones.")
        return finding("H_NUMERAL_XREF", "Serious", "pass",
                       "All %d numerals appear in both the specification and the "
                       "drawings." % len(spec_nums))
    return finding("H_NUMERAL_XREF", "Serious", "cannot_assess",
                   "Drawings supplied as images; numerals must be read visually.")


@check("H_FIGURE_LIST", "Serious", "Every figure is described and every described figure exists",
       covers=["H15"])
def figure_list(p, intake):
    described = set(p["reference_numerals"]["figures_referenced"])
    dwg = p.get("drawings") or {}
    labelled = set(dwg.get("figures_labelled") or [])
    if not described and not labelled:
        return finding("H_FIGURE_LIST", "Serious", "cannot_assess",
                       "No figure references found in the text and no drawings parsed.")
    if not labelled:
        return finding("H_FIGURE_LIST", "Serious", "cannot_assess",
                       "Text references figures %s but no drawing labels were "
                       "readable." % sorted(described))
    miss_dwg = sorted(described - labelled)
    miss_txt = sorted(labelled - described)
    if miss_dwg or miss_txt:
        return finding("H_FIGURE_LIST", "Serious", "fail",
                       "Described but not drawn: %s. Drawn but not described: %s."
                       % (miss_dwg or "none", miss_txt or "none"),
                       location="drawings / brief description",
                       fix="Reconcile the Brief Description of the Drawings with "
                           "the sheets actually filed.")
    return finding("H_FIGURE_LIST", "Serious", "pass",
                   "Figures %s are both described and drawn." % sorted(described))


@check("H_NUMERAL_CONSISTENCY", "Serious", "Each numeral labels one part consistently",
       covers=["H03"])
def numeral_consistency(p, intake):
    inc = p["reference_numerals"]["inconsistent_labels"]
    if not p["reference_numerals"]["numerals"]:
        return finding("H_NUMERAL_CONSISTENCY", "Serious", "cannot_assess",
                       "No reference numerals detected in the detailed description.")
    if inc:
        return finding(
            "H_NUMERAL_CONSISTENCY", "Serious", "cannot_assess",
            "%d numerals are preceded by more than one noun. Some are legitimate "
            "(adjectives vary: 'upper housing 10' / 'housing 10'); a model must "
            "confirm none labels two different parts." % len(inc),
            location="detailed description", candidates=inc,
            fix="One numeral, one part, one name, throughout.")
    return finding("H_NUMERAL_CONSISTENCY", "Serious", "pass",
                   "Every numeral is used with a single consistent label.")


# --------------------------------------------------------------- spec formalities

@check("F_SECTIONS", "Serious", "Required specification sections present and ordered",
       covers=["E23"])
def sections_present(p, intake):
    required = ["field", "background", "summary", "drawing_description",
                "detailed_description", "claims", "abstract"]
    missing = [s for s in required if s not in p["sections_found"]]
    order = [s for s in p["section_order"] if s in required]
    expected = [s for s in required if s in order]
    if missing:
        return finding("F_SECTIONS", "Serious", "fail",
                       "Missing required section(s): %s" % ", ".join(missing),
                       location="specification",
                       fix="Add the missing section headings and content.")
    if order != expected:
        return finding("F_SECTIONS", "Serious", "fail",
                       "Sections are out of the conventional order. Found: %s"
                       % " > ".join(order), location="specification",
                       fix="Reorder to: %s" % " > ".join(expected))
    return finding("F_SECTIONS", "Serious", "pass",
                   "All required sections present in conventional order.")


@check("F_ABSTRACT_LENGTH", "Serious", "Abstract is a single paragraph under 150 words",
       covers=["F26"])
def abstract_length(p, intake):
    a = p["abstract"]
    if not a["text"].strip():
        return finding("F_ABSTRACT_LENGTH", "Serious", "fail",
                       "No abstract found.", location="abstract",
                       fix="Add an abstract of a single paragraph, under 150 words.")
    if a["word_count"] > 150:
        return finding("F_ABSTRACT_LENGTH", "Serious", "fail",
                       "Abstract is %d words; the limit is 150." % a["word_count"],
                       location="abstract", evidence=a["text"][:200],
                       fix="Cut to 150 words or fewer.")
    return finding("F_ABSTRACT_LENGTH", "Serious", "pass",
                   "Abstract is %d words." % a["word_count"])


@check("I_PAGE_FORMAT", "Serious", "Sheet size and margins",
       covers=["I01", "I02"])
def page_format(p, intake):
    pdf = p.get("pdf")
    if not pdf:
        return finding("I_PAGE_FORMAT", "Serious", "cannot_assess",
                       "Draft was not supplied as PDF; sheet size and margins "
                       "cannot be measured.")
    LETTER = (612.0, 792.0)
    A4 = (595.0, 842.0)
    sizes = {(round(pg["width_pt"]), round(pg["height_pt"])) for pg in pdf["pages"]}
    if len(sizes) > 1:
        return finding("I_PAGE_FORMAT", "Serious", "fail",
                       "Mixed sheet sizes in one document: %s" % sorted(sizes),
                       location="whole document",
                       fix="Use one uniform sheet size throughout.")
    w, h = next(iter(sizes))
    ok = (abs(w - LETTER[0]) < 6 and abs(h - LETTER[1]) < 6) or \
         (abs(w - A4[0]) < 6 and abs(h - A4[1]) < 6)
    if not ok:
        return finding("I_PAGE_FORMAT", "Serious", "fail",
                       "Sheet is %dx%d pt, neither US Letter (612x792) nor A4 "
                       "(595x842)." % (w, h), location="whole document",
                       fix="Reformat to US Letter or A4.")
    return finding("I_PAGE_FORMAT", "Serious", "pass",
                   "%d sheets, uniform %dx%d pt." % (len(pdf["pages"]), w, h))


# ----------------------------------------------------------------- fees & entity

# Illustrative 37 CFR 1.16 tiers used only to check claim-count arithmetic.
# Dollar amounts go stale. Re-verify against the current USPTO fee schedule
# before relying on a computed total.
FEE_SCHEDULE = {
    "basic_filing": {"large": 320, "small": 160, "micro": 80},
    "search": {"large": 700, "small": 350, "micro": 175},
    "examination": {"large": 800, "small": 400, "micro": 200},
    "each_claim_over_20": {"large": 100, "small": 50, "micro": 25},
    "each_indep_over_3": {"large": 480, "small": 240, "micro": 120},
    "multiple_dependent": {"large": 860, "small": 430, "micro": 215},
}


@check("I_FEE_ARITHMETIC", "Serious", "Claim-count fee arithmetic",
       covers=["I14"])
def fees(p, intake):
    entity = (intake or {}).get("entity_status")
    if entity not in ("large", "small", "micro"):
        return finding("I_FEE_ARITHMETIC", "Serious", "cannot_assess",
                       "entity_status not supplied in intake (large|small|micro); "
                       "fee tier cannot be computed.")
    cc = p["claim_counts"]
    over20 = max(0, cc["total"] - 20)
    over3 = max(0, cc["independent"] - 3)
    lines, total = [], 0
    for key, qty in (("basic_filing", 1), ("search", 1), ("examination", 1),
                     ("each_claim_over_20", over20), ("each_indep_over_3", over3),
                     ("multiple_dependent", 1 if cc["multiple_dependent"] else 0)):
        if qty:
            amt = FEE_SCHEDULE[key][entity] * qty
            total += amt
            lines.append("%s x%d = $%d" % (key, qty, amt))
    return finding(
        "I_FEE_ARITHMETIC", "Serious", "cannot_assess",
        "Computed from %d claims (%d independent) at %s entity: %s. TOTAL $%d "
        "using illustrative 37 CFR 1.16 tiers — these MUST be re-verified against "
        "the current USPTO fee schedule before filing."
        % (cc["total"], cc["independent"], entity, "; ".join(lines), total),
        location="fee transmittal",
        candidates={"entity": entity, "counts": cc, "lines": lines,
                    "illustrative_total_dollars": total},
        fix="Confirm each amount at uspto.gov/learning-and-resources/fees-and-payment.")


@check("I_EXCESS_CLAIMS", "Quality", "Claim count against the fee thresholds",
       covers=["G63", "G64", "I14"])
def excess_claims(p, intake):
    cc = p["claim_counts"]
    msgs = []
    if cc["total"] > 20:
        msgs.append("%d total claims exceeds the 20 included" % cc["total"])
    if cc["independent"] > 3:
        msgs.append("%d independent claims exceeds the 3 included" % cc["independent"])
    if cc["multiple_dependent"]:
        msgs.append("%d multiple-dependent claim(s) incur a separate surcharge and "
                    "count as their several dependencies" % cc["multiple_dependent"])
    if msgs:
        return finding("I_EXCESS_CLAIMS", "Quality", "fail", "; ".join(msgs),
                       location="claims",
                       fix="Either accept the excess-claim fees deliberately or "
                           "consolidate before filing.")
    return finding("I_EXCESS_CLAIMS", "Quality", "pass",
                   "%d claims, %d independent — within the fee-included limits."
                   % (cc["total"], cc["independent"]))


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("parsed", help="parsed.json from parse_application.py")
    ap.add_argument("-o", "--out", default="findings_mechanical.json")
    ap.add_argument("--intake", help="intake.yaml/json for entity status etc.")
    args = ap.parse_args()

    p = json.load(open(args.parsed, encoding="utf-8"))
    intake = {}
    if args.intake:
        raw = open(args.intake, encoding="utf-8").read()
        try:
            import yaml
            intake = yaml.safe_load(raw) or {}
        except ImportError:
            try:
                intake = json.loads(raw)
            except ValueError:
                sys.exit("intake file is YAML but PyYAML is not installed: "
                         "pip install pyyaml (or supply JSON)")

    results, diagnostics = [], []
    for item_id, severity, title, covers, fn in CHECKS:
        try:
            r = fn(p, intake)
        except Exception as exc:                      # a broken check must not pass
            r = finding(item_id, severity, "cannot_assess",
                        "check raised %s: %s" % (type(exc).__name__, exc))
        r["covers"] = list(covers)
        diagnostics.append(r)
        # Credit the checklist items this check contributes to, so coverage
        # accounting reflects the mechanical pass.
        for cid in covers:
            c = dict(r, item_id=cid, source="mechanical:%s" % item_id)
            c.pop("covers", None)
            results.append(c)
    results.extend(diagnostics)
    json.dump(results, open(args.out, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)

    tally = {}
    for r in diagnostics:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    width = max(len(r["item_id"]) for r in diagnostics)
    for r in diagnostics:
        mark = {"pass": "PASS", "fail": "FAIL", "cannot_assess": "????",
                "not_applicable": " n/a"}[r["verdict"]]
        print("%s  %-*s  %s" % (mark, width, r["item_id"], r["explanation"][:150]))
    print("\n%s  ->  %s" % (", ".join("%s=%d" % kv for kv in sorted(tally.items())),
                            args.out))


if __name__ == "__main__":
    main()
