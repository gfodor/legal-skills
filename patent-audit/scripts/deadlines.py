#!/usr/bin/env python3
"""Compute every pre-filing-relevant date from the intake facts.

Date arithmetic is the single thing in this audit a language model is least
suited to and a script is best at, so no agent is asked to compute a deadline.
The agent interprets what the script returns.

    python deadlines.py intake.yaml [-o deadlines.json] [--asof YYYY-MM-DD]

Intervals implemented are those in 35 U.S.C. §§ 102, 119, 120, 122, 184 and
37 CFR 1.7, 1.78, 1.97, 1.213, 5.11 that are set, triggered, or foreclosed at
or before the filing of a regular utility application. Re-verify against the
current official text before relying on any date.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta

FITF = date(2013, 3, 16)   # America Invents Act first-inventor-to-file cutover

# US federal holidays that fall on fixed dates. Floating holidays are resolved
# below. The PTO also rolls a deadline that lands on a DC-closed day.
FIXED_HOLIDAYS = [(1, 1), (6, 19), (7, 4), (11, 11), (12, 25)]


def nth_weekday(year, month, weekday, n):
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def last_weekday(year, month, weekday):
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def federal_holidays(year):
    out = set()
    for m, d in FIXED_HOLIDAYS:
        h = date(year, m, d)
        if h.weekday() == 5:          # Saturday -> observed Friday
            h -= timedelta(days=1)
        elif h.weekday() == 6:        # Sunday -> observed Monday
            h += timedelta(days=1)
        out.add(h)
    out.add(nth_weekday(year, 1, 0, 3))    # MLK Day
    out.add(nth_weekday(year, 2, 0, 3))    # Presidents' Day
    out.add(last_weekday(year, 5, 0))      # Memorial Day
    out.add(nth_weekday(year, 9, 0, 1))    # Labor Day
    out.add(nth_weekday(year, 10, 0, 2))   # Columbus Day
    out.add(nth_weekday(year, 11, 3, 4))   # Thanksgiving
    return out


def roll(d):
    """Roll a deadline forward off weekends and DC federal holidays."""
    hol = federal_holidays(d.year) | federal_holidays(d.year + 1)
    moved = False
    while d.weekday() >= 5 or d in hol:
        d += timedelta(days=1)
        moved = True
    return d, moved


def add_months(d, months):
    y, m = divmod(d.month - 1 + months, 12)
    y, m = d.year + y, m + 1
    day = d.day
    while True:
        try:
            return date(y, m, day)
        except ValueError:
            day -= 1        # 31 Jan + 1 month -> 28/29 Feb


def parse_date(v, field):
    if v in (None, "", "none", "None"):
        return None
    if isinstance(v, date):
        return v
    try:
        y, m, d = (int(x) for x in str(v).strip().split("-"))
        return date(y, m, d)
    except Exception:
        sys.exit("intake.%s is not an ISO date (YYYY-MM-DD): %r" % (field, v))


def entry(name, trigger, trigger_date, due, consequence, blocking, asof, authority):
    due_rolled, moved = roll(due)
    days = (due_rolled - asof).days
    return {
        "deadline": name,
        "trigger": trigger,
        "trigger_date": trigger_date.isoformat(),
        "due": due_rolled.isoformat(),
        "raw_due": due.isoformat(),
        "rolled_off_weekend_or_holiday": moved,
        "days_remaining": days,
        "status": "MISSED" if days < 0 else ("URGENT" if days <= 30 else "ok"),
        "consequence_if_missed": consequence,
        "blocking": blocking,
        "authority": authority,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("intake")
    ap.add_argument("-o", "--out", default="deadlines.json")
    ap.add_argument("--asof", help="evaluate as of this date (default: today)")
    args = ap.parse_args()

    raw = open(args.intake, encoding="utf-8").read()
    try:
        import yaml
        cfg = yaml.safe_load(raw) or {}
    except ImportError:
        try:
            cfg = json.loads(raw)
        except ValueError:
            sys.exit("intake is YAML but PyYAML is missing: pip install pyyaml")

    asof = parse_date(args.asof, "asof") if args.asof else date.today()

    first_disc = parse_date(cfg.get("first_public_disclosure_date"),
                            "first_public_disclosure_date")
    first_sale = parse_date(cfg.get("first_offer_for_sale_date"),
                            "first_offer_for_sale_date")
    first_use = parse_date(cfg.get("first_public_use_date"), "first_public_use_date")
    ppa = parse_date(cfg.get("ppa_filing_date"), "ppa_filing_date")
    parent = parse_date(cfg.get("parent_filing_date"), "parent_filing_date")
    planned = parse_date(cfg.get("planned_filing_date"), "planned_filing_date")
    foreign_intent = bool(cfg.get("foreign_filing_intended"))
    nonpub = bool(cfg.get("nonpublication_request_planned"))
    disclosure_by = (cfg.get("disclosure_made_by") or "").strip().lower()

    out, warnings = [], []

    # ---- grace period on the inventor's own disclosure
    triggers = [("public disclosure", first_disc), ("offer for sale", first_sale),
                ("public use", first_use)]
    earliest = sorted([(d, n) for n, d in triggers if d], key=lambda t: t[0])
    if earliest:
        d0, label = earliest[0]
        if d0 >= FITF:
            if disclosure_by in ("inventor", "from_inventor", "obtained_from_inventor"):
                out.append(entry(
                    "AIA grace period expires", label, d0, add_months(d0, 12),
                    "The one-year grace period lapses and the inventor's own "
                    "disclosure becomes prior art barring the application.",
                    True, asof, "35 U.S.C. § 102(b)(1)"))
            else:
                warnings.append(
                    "A %s occurred on %s (post-FITF) and intake does not record it "
                    "as made by, or derived from, the inventor. If a third party "
                    "disclosed independently, there is NO grace period and U.S. "
                    "rights may already be lost. Resolve before filing."
                    % (label, d0.isoformat()))
                out.append(entry(
                    "AIA grace period expires (ONLY if inventor-derived)", label, d0,
                    add_months(d0, 12),
                    "If the disclosure was not the inventor's or derived from the "
                    "inventor, it is prior art immediately and no grace period applies.",
                    True, asof, "35 U.S.C. § 102(a)(1), (b)(1)"))
        else:
            out.append(entry(
                "Pre-FITF one-year statutory bar", label, d0, add_months(d0, 12),
                "The pre-AIA one-year grace period lapses; the U.S. application "
                "is barred.", True, asof, "pre-AIA 35 U.S.C. § 102(b)"))

        if foreign_intent:
            out.append({
                "deadline": "Foreign rights already at risk",
                "trigger": label, "trigger_date": d0.isoformat(),
                "due": "BEFORE " + d0.isoformat(),
                "raw_due": d0.isoformat(),
                "rolled_off_weekend_or_holiday": False,
                "days_remaining": None,
                "status": "MISSED",
                "consequence_if_missed":
                    "Most countries apply absolute novelty with no grace period. A "
                    "public disclosure before the U.S. filing forfeits rights in "
                    "those countries. Confirm which jurisdictions remain available.",
                "blocking": True, "authority": "Paris Convention; 35 U.S.C. § 119",
            })

    # ---- PPA
    if ppa:
        out.append(entry(
            "PPA -> regular application (U.S.)", "PPA filing", ppa,
            add_months(ppa, 12),
            "Benefit of the PPA filing date is lost entirely; the PPA becomes "
            "worthless.", True, asof, "35 U.S.C. § 119(e)"))
        out.append(entry(
            "PPA -> foreign / PCT Convention year", "PPA filing", ppa,
            add_months(ppa, 12),
            "Loss of the PPA priority date for all foreign filings.",
            bool(foreign_intent), asof, "35 U.S.C. § 119; Paris Art. 4"))

    # ---- dates that run from the filing itself
    if planned:
        out.append(entry(
            "Paris Convention year (foreign filings)", "planned U.S. filing", planned,
            add_months(planned, 12),
            "Loss of the U.S. priority date for Convention filings.",
            bool(foreign_intent), asof, "35 U.S.C. § 119; Paris Art. 4"))
        out.append(entry(
            "PCT national phase (30 months from priority)", "planned U.S. filing",
            planned, add_months(planned, 30),
            "National-phase entry barred in PCT states.", False, asof, "PCT Arts. 22, 39"))
        out.append(entry(
            "Statutory publication at 18 months", "planned U.S. filing", planned,
            add_months(planned, 18),
            "The application publishes unless a Nonpublication Request was filed "
            "WITH the application, or it has issued or gone abandoned.",
            False, asof, "35 U.S.C. § 122(b); 37 CFR 1.211"))
        out.append(entry(
            "Information Disclosure Statement due", "planned U.S. filing", planned,
            add_months(planned, 3),
            "After three months an IDS needs a fee or a certification; the duty of "
            "candour runs from filing regardless.", False, asof, "37 CFR 1.56, 1.97"))
        out.append(entry(
            "Foreign filing licence / 6-month wait", "planned U.S. filing", planned,
            add_months(planned, 6),
            "Filing abroad before a licence issues (normally granted on the filing "
            "receipt) or before six months elapse risks penalties and loss of the "
            "U.S. patent.", bool(foreign_intent), asof, "35 U.S.C. §§ 184–186; 37 CFR 5.11"))

    if parent:
        out.append({
            "deadline": "Copendency with parent application",
            "trigger": "parent filing", "trigger_date": parent.isoformat(),
            "due": "before parent issues or goes abandoned",
            "raw_due": None, "rolled_off_weekend_or_holiday": False,
            "days_remaining": None,
            "status": "check",
            "consequence_if_missed":
                "A continuation, divisional or CIP must be filed while the parent "
                "is still pending. Confirm the parent's current status.",
            "blocking": True, "authority": "35 U.S.C. § 120",
        })

    # ---- conflicts that are not date arithmetic but are date-adjacent
    if nonpub and foreign_intent:
        warnings.append(
            "CONFLICT: a Nonpublication Request is planned AND foreign filing is "
            "intended. The request certifies the invention will not be the subject "
            "of an application filed abroad. Filing abroad without rescinding it "
            "within 45 days abandons the U.S. application. Drop one or the other.")
    if planned and ppa and planned > add_months(ppa, 12):
        warnings.append(
            "The planned filing date %s is AFTER the PPA's 12-month anniversary %s. "
            "The PPA priority claim is already lost."
            % (planned.isoformat(), add_months(ppa, 12).isoformat()))

    result = {
        "as_of": asof.isoformat(),
        "fitf_cutover": FITF.isoformat(),
        "deadlines": sorted(out, key=lambda e: (e["days_remaining"] is None,
                                                e["days_remaining"])),
        "warnings": warnings,
        "missing_intake_fields": [k for k in (
            "first_public_disclosure_date", "planned_filing_date",
            "foreign_filing_intended", "entity_status") if k not in cfg],
        "note": "Intervals from 35 U.S.C. §§ 102, 119, 120, 122, 184 and "
                "37 CFR 1.7, 1.78, 1.97, 1.213, 5.11. Weekend/holiday rollover "
                "applied under 37 CFR 1.7. Confirm against current official text "
                "before relying on any date.",
    }
    json.dump(result, open(args.out, "w", encoding="utf-8"), indent=1)

    print("as of %s\n" % asof)
    for e in result["deadlines"]:
        dr = e["days_remaining"]
        print("  [%-6s] %-46s due %-12s %s" % (
            e["status"], e["deadline"][:46], e["due"],
            "" if dr is None else "(%+d days)" % dr))
    for w in warnings:
        print("\n  !! %s" % w)
    if result["missing_intake_fields"]:
        print("\n  missing intake fields: %s"
              % ", ".join(result["missing_intake_fields"]))
    print("\nwrote %s" % args.out)


if __name__ == "__main__":
    main()
