#!/usr/bin/env python3
"""Merge all findings into one ranked report with honest coverage accounting.

    python synthesize.py FINDINGS_DIR [-o audit_report.md] [--json report.json]
                         [--deadlines deadlines.json]

Reads every *.json in FINDINGS_DIR (agent output plus findings_mechanical.json),
joins them to the checklist by item_id, and reports what was assessed, what
failed, and — the part most audits omit — what could not be assessed and why.

An item with no finding from any source is reported as `not_reached`. Silence
is never counted as a pass.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "..", "reference", "checklist_index.json")

SEV_ORDER = {"Fatal": 0, "Serious": 1, "Quality": 2}
VERDICTS = ("fail", "cannot_assess", "pass", "not_applicable", "not_reached")


def load_findings(d):
    out = []
    for fn in sorted(glob.glob(os.path.join(d, "*.json"))):
        if os.path.basename(fn) in ("deadlines.json", "parsed.json"):
            continue
        try:
            data = json.load(open(fn, encoding="utf-8"))
        except ValueError as e:
            print("  ! skipping %s: %s" % (os.path.basename(fn), e))
            continue
        if isinstance(data, dict):
            data = data.get("findings", [])
        for f in data:
            if isinstance(f, dict) and f.get("item_id"):
                f.setdefault("source", os.path.basename(fn).replace(".json", ""))
                out.append(f)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("findings_dir")
    ap.add_argument("-o", "--out", default="audit_report.md")
    ap.add_argument("--json", dest="jsonout")
    ap.add_argument("--deadlines")
    ap.add_argument("--title", default="Pre-filing patent application audit")
    args = ap.parse_args()

    index = {it["id"]: it for it in json.load(open(INDEX, encoding="utf-8"))}
    findings = load_findings(args.findings_dir)

    # An item may be reported by more than one agent; keep the worst verdict.
    worst = {}
    extra = []
    for f in findings:
        iid = f["item_id"]
        if iid not in index:
            extra.append(f)          # e.g. the mechanical checks' own IDs
            continue
        prev = worst.get(iid)
        if prev is None or VERDICTS.index(f.get("verdict", "not_reached")) < \
                VERDICTS.index(prev.get("verdict", "not_reached")):
            worst[iid] = f

    rows = []
    for iid, it in index.items():
        f = worst.get(iid)
        rows.append({
            "id": iid, "part": it["part"], "part_title": it["part_title"],
            "section": it["section"], "title": it["title"], "check": it["check"],
            "severity": it["severity"],
            "verdict": (f or {}).get("verdict", "not_reached"),
            "location": (f or {}).get("location", ""),
            "evidence": (f or {}).get("evidence", ""),
            "explanation": (f or {}).get("explanation", ""),
            "suggested_fix": (f or {}).get("suggested_fix", ""),
            "source": (f or {}).get("source", ""),
            "verified_by": (f or {}).get("verified_by", ""),
        })
    rows.sort(key=lambda r: (VERDICTS.index(r["verdict"]),
                             SEV_ORDER.get(r["severity"], 3), r["id"]))

    tally = Counter(r["verdict"] for r in rows)
    bypart = defaultdict(Counter)
    for r in rows:
        bypart[r["part"]][r["verdict"]] += 1

    fails = [r for r in rows if r["verdict"] == "fail"]
    blockers = [r for r in fails if r["severity"] == "Fatal"]
    unknown = [r for r in rows if r["verdict"] == "cannot_assess"]
    unreached = [r for r in rows if r["verdict"] == "not_reached"]

    dl = json.load(open(args.deadlines, encoding="utf-8")) if args.deadlines else None

    L = []
    w = L.append
    w("# %s\n" % args.title)
    if blockers:
        w("> **DO NOT FILE.** %d fatal item(s) failed. See *Blocking* below.\n"
          % len(blockers))
    elif fails:
        w("> %d item(s) failed, none fatal. Resolve or accept each before filing.\n"
          % len(fails))
    elif unreached or unknown:
        w("> No failures, but %d item(s) could not be assessed and %d were never "
          "reached. Coverage is incomplete.\n" % (len(unknown), len(unreached)))
    else:
        w("> All %d items assessed and passed.\n" % len(rows))

    w("## Coverage\n")
    w("| Verdict | Count |\n|---|---:|")
    for v in VERDICTS:
        w("| %s | %d |" % (v, tally.get(v, 0)))
    w("| **total** | **%d** |\n" % len(rows))

    w("| Part | fail | cannot_assess | not_reached | pass | n/a |\n"
      "|---|---:|---:|---:|---:|---:|")
    for p in sorted(bypart):
        c = bypart[p]
        w("| %s %s | %d | %d | %d | %d | %d |" % (
            p, index and next(r["part_title"] for r in rows if r["part"] == p),
            c["fail"], c["cannot_assess"], c["not_reached"], c["pass"],
            c["not_applicable"]))
    w("")

    if dl:
        w("## Deadlines\n")
        bad = [e for e in dl["deadlines"] if e["status"] in ("MISSED", "URGENT")]
        if bad:
            w("| Status | Deadline | Due | Days | Consequence |\n|---|---|---|---:|---|")
            for e in bad:
                w("| **%s** | %s | %s | %s | %s |" % (
                    e["status"], e["deadline"], e["due"],
                    "" if e["days_remaining"] is None else e["days_remaining"],
                    e["consequence_if_missed"]))
            w("")
        for wn in dl.get("warnings", []):
            w("> %s\n" % wn)

    def block(title, items, body=True):
        if not items:
            return
        w("---\n\n## %s (%d)\n" % (title, len(items)))
        for r in items:
            w("### `%s` %s — %s" % (r["id"], r["title"], r["severity"]))
            w("*Part %s · %s*  \n**Check:** %s\n" % (r["part"], r["section"], r["check"]))
            if body:
                if r["location"]:
                    w("**Where:** %s  " % r["location"])
                if r["explanation"]:
                    w("**Finding:** %s  " % r["explanation"])
                if r["evidence"]:
                    w("\n> %s\n" % r["evidence"].replace("\n", "\n> "))
                if r["suggested_fix"]:
                    w("**Fix:** %s  " % r["suggested_fix"])
                if r["verified_by"]:
                    w("*Independently verified by: %s*  " % r["verified_by"])
            w("")

    block("Blocking — must be resolved before filing", blockers)
    block("Failed — not fatal", [r for r in fails if r["severity"] != "Fatal"])
    block("Could not be assessed", unknown)

    if unreached:
        w("---\n\n## Not reached (%d)\n" % len(unreached))
        w("No agent reported on these. Either the owning agent did not run, or it "
          "silently skipped them. Treat as unaudited, not as passing.\n")
        w("| ID | Severity | Check |\n|---|---|---|")
        for r in unreached:
            w("| `%s` | %s | %s |" % (r["id"], r["severity"], r["check"][:110]))
        w("")

    if extra:
        w("---\n\n## Mechanical pre-pass results\n")
        w("Deterministic checks that do not map onto a single checklist item.\n")
        w("| Check | Verdict | Detail |\n|---|---|---|")
        for f in extra:
            w("| `%s` | %s | %s |" % (f["item_id"], f.get("verdict", ""),
                                      f.get("explanation", "")[:160].replace("|", "\\|")))
        w("")

    w("---\n\n*Checklist: %d items grounded in 35 U.S.C., 37 CFR, the MPEP, "
      "and current USPTO practice. Fee amounts and form names must be "
      "re-verified against the current official fee schedule and forms page. "
      "Not legal advice.*" % len(rows))

    open(args.out, "w", encoding="utf-8").write("\n".join(L))
    if args.jsonout:
        json.dump({"summary": dict(tally), "rows": rows,
                   "mechanical_extra": extra, "deadlines": dl},
                  open(args.jsonout, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)

    print("coverage: " + ", ".join("%s=%d" % (v, tally.get(v, 0)) for v in VERDICTS))
    print("blocking: %d   failed: %d   unknown: %d   unreached: %d"
          % (len(blockers), len(fails), len(unknown), len(unreached)))
    print("wrote %s" % args.out)
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
