#!/usr/bin/env python3
"""Drive the shipped audit scripts and reject book-extraction residue.

This is not a string-list unit test of a reimplementation. It:
  1. walks the shipped skill tree for forbidden attribution strings
  2. checks every checklist item in the part files has a Primary source cite
  3. runs parse_application / mechanical_checks / deadlines / synthesize
     (the same entry points prepass.py shells out to) on assets/sample_draft.md
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
# Live installs that must stay in lockstep with this skill.
SIBLING_TREES = [
    os.path.join(os.path.expanduser("~"), ".grok", "skills", "patent-audit"),
    os.path.join(os.path.expanduser("~"), "skills", "patent-audit"),
    os.path.join(os.path.expanduser("~"), ".codex", "skills", "patent-audit"),
]

# Patterns assembled at runtime so this test file itself is not a hit list.
FORBIDDEN = [
    "".join(("Patent", " It ", "Yourself")),
    "".join(("Press", "man")),
    r"\b" + "No" + "lo" + r"\b",
    "".join(("Book", " support")),
    "Inventor.?" + "s Commandment",
    r"\b" + "Le" + "Roy" + r"\b",
    r"\b" + "Grisel" + "da" + r"\b",
    r"\b" + "Mil" + "lie" + r"\b",
    "Sam " + "Searcher",
    r"\b" + "Pre" + "witt" + r"\b",
    "extracted" + " from",
    "book " + "Appendix",
    "book" + "_page",
    r"\(p\. \d",
    r"pp\. \d{2,}",
]

SKIP_DIR_NAMES = {".git", "__pycache__", ".venv", "venv"}
SKIP_FILES = {os.path.basename(__file__)}


def die(msg):
    print("FAIL:", msg, file=sys.stderr)
    raise SystemExit(1)


def walk_tree(root):
    if not os.path.isdir(root):
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            if name in SKIP_FILES:
                continue
            path = os.path.join(dirpath, name)
            if os.path.splitext(name)[1].lower() in {
                ".md", ".py", ".yaml", ".yml", ".json", ".txt"
            } or name in {".gitignore"}:
                yield path


def shipped_files():
    seen = set()
    for root in [REPO] + SIBLING_TREES:
        for path in walk_tree(root):
            key = os.path.normcase(os.path.abspath(path))
            if key in seen:
                continue
            seen.add(key)
            yield path


def test_no_forbidden_strings():
    hits = []
    compiled = [(pat, re.compile(pat, re.I)) for pat in FORBIDDEN]
    for path in shipped_files():
        try:
            text = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        for pat, rx in compiled:
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                rel = os.path.relpath(path, REPO)
                hits.append("%s:%d: %s" % (rel, line, pat))
    if hits:
        die("forbidden attribution still present:\n  " + "\n  ".join(hits[:40]))
    print("ok  no forbidden attribution strings in shipped tree")


def test_part_files_are_primary_source():
    index = json.load(open(os.path.join(ROOT, "reference", "checklist_index.json"),
                           encoding="utf-8"))
    by_part = {}
    for item in index:
        by_part.setdefault(item["part"], []).append(item["id"])

    parts_dir = os.path.join(ROOT, "reference", "parts")
    sampled = []
    for part, ids in sorted(by_part.items()):
        matches = [n for n in os.listdir(parts_dir) if n.startswith(part + "_")]
        if len(matches) != 1:
            die("expected one part file for %s, found %s" % (part, matches))
        text = open(os.path.join(parts_dir, matches[0]), encoding="utf-8").read()
        if "".join(("Book", " support")) in text:
            die("%s still has quoted-guide support blocks" % matches[0])
        found_ids = re.findall(r"^### `([A-Z]\d+)`", text, re.M)
        if found_ids != ids:
            die("%s item ids %s != index %s" % (matches[0], found_ids, ids))
        for item_id in ids:
            chunk = text.split("### `%s`" % item_id, 1)[1]
            next_h = re.search(r"\n### `", chunk)
            if next_h:
                chunk = chunk[:next_h.start()]
            if "**Primary source:**" not in chunk:
                die("%s has no Primary source cite" % item_id)
            if not re.search(r"35 U\.S\.C\.|37 CFR|MPEP|USPTO|uspto\.gov|Alice|Paris|PCT|EPC",
                             chunk):
                die("%s Primary source does not name a statute/rule/MPEP/official page"
                    % item_id)
        sampled.append("%s:%s" % (part, ids[0]))
    print("ok  %d items across parts %s have Primary source cites"
          % (sum(len(v) for v in by_part.values()), ", ".join(sampled)))


def run_script(name, *args):
    cmd = [sys.executable, os.path.join(HERE, name), *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        die("%s exited %s\n%s\n%s" % (name, proc.returncode, proc.stdout, proc.stderr))
    return proc


def test_shipped_scripts_on_sample_draft():
    draft = os.path.join(ROOT, "assets", "sample_draft.md")
    if not os.path.exists(draft):
        die("missing sample draft %s" % draft)

    intake_body = """\
planned_filing_date: 2026-09-01
application_type: utility
entity_status: small
first_public_disclosure_date: 2025-10-01
disclosure_made_by: inventor
ppa_filing_date: 2025-11-01
foreign_filing_intended: false
nonpublication_request_planned: false
"""
    with tempfile.TemporaryDirectory() as wd:
        intake = os.path.join(wd, "intake.yaml")
        open(intake, "w", encoding="utf-8").write(intake_body)
        parsed = os.path.join(wd, "parsed.json")
        findings_dir = os.path.join(wd, "findings")
        os.makedirs(findings_dir)
        mechanical = os.path.join(findings_dir, "findings_mechanical.json")
        deadlines = os.path.join(wd, "deadlines.json")
        report = os.path.join(wd, "audit_report.md")

        p = run_script("parse_application.py", draft, "-o", parsed)
        print(p.stdout.strip() or "parse_application ran")
        data = json.load(open(parsed, encoding="utf-8"))
        if not data.get("claims"):
            die("parse_application produced no claims")

        run_script("mechanical_checks.py", parsed, "--intake", intake, "-o", mechanical)
        run_script("deadlines.py", intake, "-o", deadlines, "--asof", "2026-08-12")
        dl = json.load(open(deadlines, encoding="utf-8"))
        dumped = json.dumps(dl)
        if "book" + "_page" in dumped:
            die("deadlines.json still embeds guide-page provenance")
        if "Patent" + " It" in dumped:
            die("deadlines.json still embeds popular-guide attribution")
        if not dl.get("deadlines"):
            die("deadlines.py produced no deadline rows")

        syn = run_script("synthesize.py", findings_dir, "--deadlines", deadlines,
                         "-o", report)
        print(syn.stdout.strip())
        body = open(report, encoding="utf-8").read()
        title = "".join(("Patent", " It ", "Yourself"))
        author = "".join(("Press", "man"))
        if re.search(r"\b%s\b|\b%s\b" % (re.escape(title), re.escape(author)),
                     body, re.I):
            die("synthesize report still attributes the checklist to a popular guide")
        if "grounded in 35 U.S.C." not in body:
            die("synthesize footer does not describe a primary-source checklist")
        print("ok  shipped scripts ran on sample_draft; report has no book footer")
        return body, syn.stdout, dl


def main():
    test_no_forbidden_strings()
    test_part_files_are_primary_source()
    test_shipped_scripts_on_sample_draft()
    print("all checks passed")


if __name__ == "__main__":
    main()
