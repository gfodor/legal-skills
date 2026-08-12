#!/usr/bin/env python3
"""Parse a draft patent application into a structured JSON fact-pack.

Every downstream agent reads this instead of raw text, so the expensive,
error-prone bookkeeping (claim dependency graphs, reference-numeral
cross-referencing, antecedent-basis candidates) happens once, in code, exactly.

    python parse_application.py DRAFT [-o parsed.json] [--drawings DIR_OR_PDF]

DRAFT may be .txt, .md, .pdf or .docx. PDF needs PyMuPDF; .docx needs python-docx.
Missing optional dependencies degrade to a clear error, never to silent partial
output.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Canonical specification sections, in the order the PTO expects them.
SECTION_PATTERNS = [
    ("title", r"^\s*(?:TITLE(?:\s+OF\s+THE\s+INVENTION)?)\s*:?\s*$"),
    ("cross_reference", r"^\s*CROSS[- ]REFERENCES?\s+TO\s+RELATED\s+APPLICATIONS?\s*:?\s*$"),
    ("federal_research", r"^\s*(?:STATEMENT\s+REGARDING\s+)?FEDERALLY[- ]SPONSORED\s+"
                         r"(?:RESEARCH|R\s*&\s*D).*$"),
    ("sequence_listing", r"^\s*(?:REFERENCE\s+TO\s+)?SEQUENCE\s+LISTING.*$"),
    ("field", r"^\s*(?:TECHNICAL\s+)?FIELD(?:\s+OF\s+THE\s+INVENTION)?\s*:?\s*$"),
    ("background", r"^\s*BACKGROUND(?:\s+OF\s+THE\s+INVENTION)?.*$"),
    ("summary", r"^\s*(?:BRIEF\s+)?SUMMARY(?:\s+OF\s+THE\s+INVENTION)?.*$"),
    ("drawing_description", r"^\s*BRIEF\s+DESCRIPTION\s+OF\s+THE\s+(?:SEVERAL\s+VIEWS\s+OF\s+THE\s+)?"
                            r"DRAWINGS?.*$"),
    ("detailed_description", r"^\s*DETAILED\s+DESCRIPTION.*$"),
    ("claims", r"^\s*(?:CLAIMS?|(?:I|WE)\s+CLAIM|WHAT\s+IS\s+CLAIMED\s+IS|"
               r"THE\s+INVENTION\s+CLAIMED\s+IS)\s*:?\s*$"),
    ("abstract", r"^\s*ABSTRACT(?:\s+OF\s+THE\s+DISCLOSURE)?\s*:?\s*$"),
]

TRANSITIONS = [
    ("comprising", r"\bcompris(?:ing|es)\b"),
    ("consisting_essentially_of", r"\bconsisting\s+essentially\s+of\b"),
    ("consisting_of", r"\bconsisting\s+of\b"),
    ("including", r"\binclud(?:ing|es)\b"),
    ("having", r"\bhaving\b"),
    ("which_comprises", r"\bwhich\s+comprises\b"),
]

# "the widget", "said upper housing" -- candidate antecedent references.
DEF_REF = re.compile(r"\b(?:the|said)\s+((?:[a-z][a-z\-]+\s+){0,4}[a-z][a-z\-]+)", re.I)
INDEF_REF = re.compile(r"\b(?:a|an)\s+((?:[a-z][a-z\-]+\s+){0,4}[a-z][a-z\-]+)", re.I)

# A noun phrase ends at any of these; without truncation "a cylindrical body of
# insulating material" registers its head as "material" and the later "said
# body" is wrongly flagged as lacking an antecedent.
NP_STOP = {
    "of", "with", "for", "that", "which", "is", "are", "was", "were", "be",
    "being", "been", "has", "have", "having", "and", "or", "to", "in", "into",
    "on", "at", "by", "from", "within", "between", "through", "over", "under",
    "comprising", "comprises", "including", "includes", "wherein", "whereby",
    "said", "the", "a", "an", "disposed", "positioned", "arranged", "coupled",
    "connected", "attached", "mounted", "secured", "formed", "extending",
    "adapted", "configured", "operable", "capable", "when", "while", "then",
    "so", "such", "thereby", "further", "also", "may", "can", "will", "shall",
}

# Words that are never the head of a claim element, so a "the <word>" hit is not
# a real antecedent-basis candidate.
NON_ELEMENT_HEADS = {
    "art", "invention", "embodiment", "figure", "drawing", "specification",
    "same", "other", "first", "second", "third", "one", "another", "above",
    "following", "present", "prior", "group", "claim", "claims", "steps",
    "step", "method", "process", "case", "event", "time", "order", "number",
    "amount", "way", "art-recognized", "user", "art recognized",
}


# --------------------------------------------------------------------------- io

def load_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md"):
        return open(path, encoding="utf-8", errors="replace").read(), None
    if ext == ".pdf":
        try:
            import fitz
        except ImportError:
            sys.exit("PDF input needs PyMuPDF:  pip install pymupdf")
        doc = fitz.open(path)
        pages = [doc[i].get_text("text") for i in range(len(doc))]
        geom = [{"page": i + 1, "width_pt": doc[i].rect.width,
                 "height_pt": doc[i].rect.height} for i in range(len(doc))]
        return "\n".join(pages), {"pages": geom, "page_texts": pages}
    if ext == ".docx":
        try:
            import docx
        except ImportError:
            sys.exit("DOCX input needs python-docx:  pip install python-docx")
        return "\n".join(p.text for p in docx.Document(path).paragraphs), None
    sys.exit("unsupported input type: %s (use .txt, .md, .pdf or .docx)" % ext)


# ---------------------------------------------------------------------- sections

def split_sections(text):
    """Locate canonical headings; return {name: {...}} plus anything before the first."""
    lines = text.split("\n")
    hits = []
    for idx, line in enumerate(lines):
        for name, pat in SECTION_PATTERNS:
            if re.match(pat, line.strip(), re.I):
                hits.append((idx, name))
                break
    out, missing = {}, []
    for i, (idx, name) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(lines)
        body = "\n".join(lines[idx + 1:end]).strip()
        # A heading may legitimately repeat (e.g. BACKGROUND then a subheading);
        # keep the first, longest occurrence.
        if name not in out or len(body) > len(out[name]["text"]):
            out[name] = {"line": idx + 1, "heading": lines[idx].strip(), "text": body}
    for name, _ in SECTION_PATTERNS:
        if name not in out:
            missing.append(name)
    preamble = "\n".join(lines[:hits[0][0]]).strip() if hits else text.strip()
    return out, missing, preamble


# ------------------------------------------------------------------------ claims

def parse_claims(claims_text):
    """Split the claim set and decompose each claim."""
    if not claims_text:
        return []
    # A claim starts at a line-leading number followed by . or )
    parts = re.split(r"(?m)^\s*(\d{1,3})\s*[\.\)]\s+", "\n" + claims_text)
    claims = []
    for i in range(1, len(parts) - 1, 2):
        num, body = int(parts[i]), parts[i + 1].strip()
        claims.append(build_claim(num, body))
    return claims


def build_claim(num, body):
    flat = re.sub(r"\s+", " ", body).strip()

    dep = re.search(
        r"\b(?:of|in|to|according\s+to|as\s+(?:set\s+forth|recited|claimed)\s+in|defined\s+in)\s+"
        r"(?:any\s+(?:one\s+)?of\s+)?claims?\s+(\d+)(?:\s*(?:-|to|through|,|or|and)\s*(\d+))?",
        flat, re.I)
    parents, multiple = [], False
    if dep:
        parents = [int(dep.group(1))]
        if dep.group(2):
            multiple = True
            parents.append(int(dep.group(2)))
        if re.search(r"any\s+(?:one\s+)?of\s+claims", flat, re.I):
            multiple = True

    transition, t_pos = None, None
    for name, pat in TRANSITIONS:
        m = re.search(pat, flat, re.I)
        if m and (t_pos is None or m.start() < t_pos):
            transition, t_pos = name, m.start()

    preamble = flat[:t_pos].strip() if t_pos is not None else flat
    rest = flat[t_pos:] if t_pos is not None else ""
    elements = [e.strip() for e in re.split(r";\s*(?:and\s+)?", rest) if e.strip()]

    return {
        "number": num,
        "text": flat,
        "type": "dependent" if parents else "independent",
        "parents": parents,
        "multiple_dependent": multiple,
        "preamble": preamble,
        "transition": transition,
        "elements": elements,
        "element_count": len(elements),
        "word_count": len(flat.split()),
        "sentence_count": flat.count(".") if flat.endswith(".") else flat.count(".") + 1,
        "ends_with_period": flat.rstrip().endswith("."),
        "internal_periods": len(re.findall(r"\.(?=\s+[A-Za-z])", flat)),
        "means_plus_function": bool(re.search(r"\bmeans\s+for\b|\bstep\s+for\b", flat, re.I)),
        "uses_whereby": bool(re.search(r"\bwhereby\b", flat, re.I)),
        "relative_terms": sorted({w.lower() for w in re.findall(
            r"\b(?:about|approximately|substantially|relatively|essentially|"
            r"generally|preferably|optionally|such\s+as|thin|thick|large|small|"
            r"strong|light|heavy|near|close)\b", flat, re.I)}),
    }


def claim_ancestry(claims):
    """Resolve each claim's full parent chain, marking cycles and dangling refs."""
    by_num = {c["number"]: c for c in claims}
    for c in claims:
        chain, seen, cur = [], set(), c
        while cur["parents"]:
            p = cur["parents"][0]
            if p in seen or p not in by_num:
                break
            seen.add(p)
            chain.append(p)
            cur = by_num[p]
        c["ancestry"] = chain
        c["dangling_parents"] = [p for p in c["parents"] if p not in by_num]
        c["forward_reference"] = [p for p in c["parents"] if p >= c["number"]]
    return claims


# -------------------------------------------------------------- antecedent basis

def noun_phrase(raw):
    """Trim a captured span down to the noun phrase itself."""
    words = []
    for w in re.split(r"\s+", raw.strip().lower()):
        if not w or w in NP_STOP:
            break
        words.append(w)
    return " ".join(words)


def phrase_forms(np):
    """Every suffix of a noun phrase, so 'a tension band' also introduces 'band'."""
    words = np.split()
    return {" ".join(words[i:]) for i in range(len(words))} if words else set()


def antecedent_candidates(claim, ancestry_text):
    """Definite references with no earlier indefinite introduction.

    Deliberately over-inclusive: a model adjudicates the list. An inherent
    property ("the length of the rod") is legitimate without an antecedent, and
    only a reader can tell that from a genuine missing element.
    """
    scope = ancestry_text + " " + claim["text"]
    introduced = set()
    for m in INDEF_REF.finditer(scope):
        introduced |= phrase_forms(noun_phrase(m.group(1)))
    # A claim's own preamble introduces its subject without an article.
    introduced |= phrase_forms(noun_phrase(
        re.sub(r"^(?:an?|the)\s+", "", claim["preamble"].strip().lower())))

    flagged, seen = [], set()
    for m in DEF_REF.finditer(claim["text"]):
        np = noun_phrase(m.group(1))
        if not np:
            continue
        head = np.split()[-1]
        if head in NON_ELEMENT_HEADS or np in NON_ELEMENT_HEADS:
            continue
        if phrase_forms(np) & introduced:
            continue
        if np in seen:
            continue
        seen.add(np)
        flagged.append({"phrase": "%s %s" % (m.group(0).split()[0], np),
                        "noun": np, "offset": m.start()})
    return flagged


# ------------------------------------------------------------ reference numerals

def reference_numerals(sections):
    """Numerals used in the description vs. those introduced in the drawing list."""
    desc = " ".join(sections.get(k, {}).get("text", "")
                    for k in ("detailed_description", "summary", "drawing_description"))
    detail_only = sections.get("detailed_description", {}).get("text", "")

    # A reference numeral follows a noun: "housing 10", "the upper plate 12a".
    pat = re.compile(r"\b([a-z][a-z\-]{2,})\s+(\d{1,3}[a-z]?)\b")
    found = {}
    for m in pat.finditer(detail_only):
        found.setdefault(m.group(2), set()).add(m.group(1).lower())
    counts = {}
    for m in re.finditer(r"\b(\d{1,3}[a-z]?)\b", detail_only):
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1

    figs = sorted({m.group(1) for m in re.finditer(
        r"\bFIGS?\.?\s*(\d+[A-Za-z]?)", desc, re.I)})

    return {
        "numerals": sorted(found, key=lambda s: (len(s), s)),
        "numeral_labels": {k: sorted(v) for k, v in sorted(found.items())},
        "numeral_mention_counts": {k: counts.get(k, 0) for k in sorted(found)},
        "single_use_numerals": sorted(k for k in found if counts.get(k, 0) < 2),
        "inconsistent_labels": {k: sorted(v) for k, v in sorted(found.items())
                                if len(v) > 1},
        "figures_referenced": figs,
    }


# ----------------------------------------------------------------------- drawings

def drawing_inventory(path):
    if not path:
        return None
    if os.path.isdir(path):
        sheets = sorted(f for f in os.listdir(path)
                        if os.path.splitext(f)[1].lower()
                        in (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".pdf"))
        return {"source": path, "sheet_count": len(sheets), "sheets": sheets}
    try:
        import fitz
    except ImportError:
        return {"source": path, "error": "PyMuPDF not installed; cannot inspect"}
    doc = fitz.open(path)
    sheets, labels = [], set()
    for i in range(len(doc)):
        t = doc[i].get_text("text")
        labels |= {m.group(1) for m in re.finditer(r"\bFIGS?\.?\s*(\d+[A-Za-z]?)", t, re.I)}
        sheets.append({"sheet": i + 1,
                       "width_pt": doc[i].rect.width, "height_pt": doc[i].rect.height,
                       "numerals": sorted({m.group(1) for m in
                                           re.finditer(r"\b(\d{1,3}[a-z]?)\b", t)}),
                       "has_text_layer": bool(t.strip())})
    return {"source": path, "sheet_count": len(sheets), "sheets": sheets,
            "figures_labelled": sorted(labels)}


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("-o", "--out", default="parsed.json")
    ap.add_argument("--drawings", help="drawing sheets: a PDF or a directory of images")
    args = ap.parse_args()

    text, pdfmeta = load_text(args.draft)
    sections, missing, preamble = split_sections(text)
    claims = claim_ancestry(parse_claims(sections.get("claims", {}).get("text", "")))

    by_num = {c["number"]: c for c in claims}
    for c in claims:
        anc = " ".join(by_num[p]["text"] for p in c["ancestry"] if p in by_num)
        c["antecedent_candidates"] = antecedent_candidates(c, anc)

    abstract = sections.get("abstract", {}).get("text", "")
    out = {
        "source": os.path.abspath(args.draft),
        "char_count": len(text),
        "word_count": len(text.split()),
        "sections_found": sorted(sections),
        "sections_missing": missing,
        "section_order": [n for n, _ in sorted(
            ((n, s["line"]) for n, s in sections.items()), key=lambda kv: kv[1])],
        "preamble_before_first_heading": preamble[:2000],
        "sections": sections,
        "title": (sections.get("title", {}).get("text", "") or preamble).strip()[:300],
        "abstract": {
            "text": abstract,
            "word_count": len(abstract.split()),
            "sentence_count": len([s for s in re.split(r"(?<=[.!?])\s+", abstract) if s.strip()]),
        },
        "claims": claims,
        "claim_counts": {
            "total": len(claims),
            "independent": sum(1 for c in claims if c["type"] == "independent"),
            "dependent": sum(1 for c in claims if c["type"] == "dependent"),
            "multiple_dependent": sum(1 for c in claims if c["multiple_dependent"]),
        },
        "reference_numerals": reference_numerals(sections),
        "drawings": drawing_inventory(args.drawings),
        "pdf": pdfmeta and {"pages": pdfmeta["pages"]},
    }
    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print("parsed  %s" % args.draft)
    print("  sections found   : %s" % ", ".join(out["sections_found"]))
    if missing:
        print("  sections missing : %s" % ", ".join(missing))
    print("  claims           : %d (%d independent, %d dependent)" % (
        out["claim_counts"]["total"], out["claim_counts"]["independent"],
        out["claim_counts"]["dependent"]))
    print("  numerals         : %d" % len(out["reference_numerals"]["numerals"]))
    print("  abstract words   : %d" % out["abstract"]["word_count"])
    print("  wrote            : %s" % args.out)


if __name__ == "__main__":
    main()
