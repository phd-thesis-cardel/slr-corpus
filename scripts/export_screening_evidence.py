"""Render the screening decisions as a readable document, grouped by question.

Derives from data/screening_decisions.json, so the document and the data cannot
disagree.

Usage:
    python3 scripts/export_screening_evidence.py
"""

from __future__ import annotations

import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DECISIONS = os.path.join(REPO, "data", "screening_decisions.json")
OUT = os.path.join(REPO, "docs", "screening-evidence.md")

CRITERIA = (
    "Studies were judged against the inclusion and exclusion criteria of the "
    "review, in particular the two exclusion clauses that read *Publications "
    "not directly related to RESTful API security or mutation testing* and "
    "*Articles focusing on non-RESTful API security or unrelated mutation "
    "testing domains*. The scope of the review admits adjacent work on web "
    "services, fault injection and stateful fuzzing, so a study is excluded "
    "only when it belongs to a different field altogether."
)


def main() -> int:
    with open(DECISIONS, encoding="utf-8") as fh:
        records = json.load(fh)
    excluded = [r for r in records if r["decision"] == "excluded"]
    included = [r for r in records if r["decision"] == "included"]

    by_rq: dict[str, list] = defaultdict(list)
    for rec in excluded:
        by_rq[(rec.get("rq") or ["unassigned"])[0]].append(rec)

    lines = [
        "---",
        "title: Screening decisions and their evidence",
        "author: Carlos A. Delgado S.",
        "version: 1.0",
        "status: final",
        "tags: [slr, prisma, screening, corpus]",
        "---",
        "",
        "# Screening decisions",
        "",
        CRITERIA,
        "",
        f"- Studies judged: **{len(records)}**",
        f"- Included: **{len(included)}**",
        f"- Excluded: **{len(excluded)}**",
        "",
        "Each exclusion carries its reason and a verbatim fragment of the source "
        "record behind it, so a decision can be checked study by study rather "
        "than accepted wholesale. The included studies are listed with their "
        "characteristics in `../data/corpus.csv`.",
        "",
        "## Excluded studies",
        "",
    ]

    for rq in sorted(by_rq):
        lines += [f"### {rq} ({len(by_rq[rq])} studies)", ""]
        for rec in sorted(by_rq[rq], key=lambda r: (r.get("authors") or "").lower()):
            venue = rec.get("venue") or "(no venue field)"
            doi = rec.get("doi") or "(no DOI)"
            lines += [f"**{rec['title']}**  ",
                      f"{rec.get('year', '')} · {venue} · {doi}", ""]
            if rec.get("exclusion_reason"):
                lines += [f"*Reason.* {rec['exclusion_reason']}", ""]
            if rec.get("exclusion_evidence"):
                lines += [f"> {rec['exclusion_evidence'].strip().strip(chr(34))}", ""]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  {len(excluded)} exclusions, {len(included)} included -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
