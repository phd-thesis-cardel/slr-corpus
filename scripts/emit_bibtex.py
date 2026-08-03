"""Emit one BibTeX entry per included study, keyed as a primary-study series.

PRISMA 2020 item 17 asks a review to cite each included study and to present its
characteristics. The characteristics table discharges the second half; this file
discharges the first. Keys follow the convention used in software-engineering
reviews, where primary studies carry their own series (S1..Sn) kept disjoint from
the methodological bibliography, so that the two can be cited side by side
without renumbering either.

Entries missing a venue are emitted with a note recording the gap rather than
silently dropped or padded, since a reader who cannot resolve an entry needs to
know that the source record itself was incomplete.

Usage:
    python3 scripts/emit_bibtex.py data/screening_decisions.json data/primary-studies.bib
"""

from __future__ import annotations

import json
import re
import sys

CONF_HINTS = ("conference", "proceedings", "symposium", "workshop", "congress")


def esc(s: str | None) -> str:
    s = (s or "").strip()
    for a, b in (("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")):
        s = s.replace(a, b)
    return s


def authors_to_bibtex(raw: str | None) -> str:
    """Normalize the three author formats present in the corpus.

    Scopus exports carry "I., Lastname, Firstname; ...", BibTeX-derived records
    carry "Lastname, Firstname and ...", and some records terminate in the
    "and others" artifact of a truncated list.
    """
    raw = (raw or "").strip()
    if not raw:
        return ""
    if " and " in raw and ";" not in raw:
        return esc(raw)
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    names = []
    for p in parts:
        bits = [b.strip() for b in p.split(",") if b.strip()]
        # "I., Lastname, Firstname" -> "Lastname, Firstname"
        if len(bits) >= 3 and len(bits[0]) <= 3 and bits[0].endswith("."):
            names.append(f"{bits[1]}, {bits[2]}")
        elif len(bits) >= 2:
            names.append(f"{bits[0]}, {bits[1]}")
        else:
            names.append(bits[0] if bits else p)
    return esc(" and ".join(names))


def entry_type(rec: dict) -> str:
    dt = (rec.get("doc_type") or "").lower()
    venue = (rec.get("venue") or "").lower()
    if "conference" in dt or "proceedings" in dt:
        return "inproceedings"
    if "book" in dt:
        return "incollection"
    if any(h in venue for h in CONF_HINTS):
        return "inproceedings"
    return "article"


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    records = json.load(open(sys.argv[1], encoding="utf-8"))
    included = [r for r in records if r["decision"] == "included"]
    included.sort(key=lambda r: ((r.get("authors") or "zz").lower(), r.get("year") or ""))

    out = [
        "% Primary studies of the systematic literature review.",
        "% One entry per included study, keyed S1..Sn.",
        f"% {len(included)} studies. Generated from screening_decisions.json.",
        "",
    ]
    no_venue = no_doi = 0
    for i, r in enumerate(included, 1):
        key = f"S{i}"
        kind = entry_type(r)
        field = "booktitle" if kind in ("inproceedings", "incollection") else "journal"
        lines = [f"@{kind}{{{key},"]
        auth = authors_to_bibtex(r.get("authors"))
        if auth:
            lines.append(f"  author    = {{{auth}}},")
        lines.append(f"  title     = {{{esc(r.get('title'))}}},")
        if r.get("venue"):
            lines.append(f"  {field:9s} = {{{esc(r['venue'])}}},")
        else:
            no_venue += 1
            lines.append("  note      = {Venue not recorded in the source database export},")
        if r.get("year"):
            lines.append(f"  year      = {{{r['year']}}},")
        if r.get("doi"):
            lines.append(f"  doi       = {{{r['doi']}}},")
        else:
            no_doi += 1
        lines.append(f"  keywords  = {{{'; '.join(r.get('rq') or [])}}},")
        lines.append("}")
        out.append("\n".join(lines))
        out.append("")

    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"  {len(included)} entries -> {sys.argv[2]}")
    print(f"  without venue: {no_venue}   without DOI: {no_doi}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
