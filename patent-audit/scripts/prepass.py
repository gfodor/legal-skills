#!/usr/bin/env python3
"""Run the whole deterministic pre-pass and scaffold the working directory.

    python prepass.py --draft DRAFT [--drawings D] [--intake intake.yaml]
                      [--workdir audit_run] [--asof YYYY-MM-DD]

With no --intake, copies the questionnaire template in and stops, because the
gates cannot run on assumed facts. Everything it produces lands in --workdir:

    parsed.json                 structured draft — every agent reads this
    deadlines.json              computed dates, rollover applied
    findings/findings_mechanical.json
    intake.yaml                 (template, if you did not supply one)
    findings/                   agents write <agent>.json here

Exits 2 if the parse looks wrong, so a bad parse cannot silently produce a
confident audit of nothing.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def run(script, *args):
    cmd = [sys.executable, os.path.join(HERE, script)] + [str(a) for a in args]
    # flush, or this banner lands after the child's output
    print("\n$ %s %s" % (script, " ".join(str(a) for a in args)), flush=True)
    return subprocess.run(cmd).returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--draft", required=True)
    ap.add_argument("--drawings")
    ap.add_argument("--intake")
    ap.add_argument("--workdir", default="audit_run")
    ap.add_argument("--asof")
    args = ap.parse_args()

    wd = os.path.abspath(args.workdir)
    os.makedirs(os.path.join(wd, "findings"), exist_ok=True)
    parsed = os.path.join(wd, "parsed.json")

    pa = ["parse_application.py", args.draft, "-o", parsed]
    if args.drawings:
        pa += ["--drawings", args.drawings]
    if run(*pa) != 0:
        return 2

    p = json.load(open(parsed, encoding="utf-8"))
    problems = []
    if not p["claims"]:
        problems.append("no claims were parsed")
    if len(p["sections_found"]) < 4:
        problems.append("only %d sections recognised: %s"
                        % (len(p["sections_found"]), p["sections_found"]))
    if not p["reference_numerals"]["numerals"] and p["sections"].get("detailed_description"):
        problems.append("no reference numerals found in the detailed description")
    if problems:
        print("\n!! The draft did not parse cleanly:")
        for x in problems:
            print("     - %s" % x)
        print("   Every downstream agent reads parsed.json, so fix the parse before\n"
              "   dispatching them — otherwise they audit a document that isn't there.\n"
              "   Usually the draft uses unusual section headings or claim numbering.")
        return 2

    intake = args.intake
    if not intake:
        dest = os.path.join(wd, "intake.yaml")
        if not os.path.exists(dest):
            shutil.copy(os.path.join(ROOT, "assets", "intake.yaml"), dest)
        print("\n!! No intake supplied. Template written to:\n     %s\n"
              "   Parts A, C and D cannot run until it is filled in. %d checklist\n"
              "   items are answerable ONLY from intake facts — no document review\n"
              "   can reach them." % (dest, count_intake_only()))
        return 1

    run("mechanical_checks.py", parsed, "--intake", intake,
        "-o", os.path.join(wd, "findings", "findings_mechanical.json"))
    dl = ["deadlines.py", intake, "-o", os.path.join(wd, "deadlines.json")]
    if args.asof:
        dl += ["--asof", args.asof]
    run(*dl)

    print("\npre-pass complete. Working directory: %s" % wd)
    print("Next: dispatch the gate agents (Phase 2), then the fan-out (Phase 3).")
    return 0


def count_intake_only():
    idx = json.load(open(os.path.join(ROOT, "reference", "checklist_index.json"),
                         encoding="utf-8"))
    return sum(1 for it in idx if it.get("inputs") == ["intake_facts"])


if __name__ == "__main__":
    raise SystemExit(main())
