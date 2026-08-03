"""Join the unified corpus with the abstracts held in the raw database exports.

The corpus file carries no abstract column, so a re-screening of the included
records against the review's own inclusion and exclusion criteria has nothing to
judge. The raw Scopus exports do carry abstracts; this script joins them back on
normalized title and writes one JSON record per study for downstream screening.

Usage:
    bash containers/run.sh slr-update python scripts/slr-update/build_screening_set.py
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys

import os as _os

# Resolve the corpus location without hard-coding anyone's home directory:
# the repository's own data/ directory by default, overridable for a working
# tree that keeps the raw vendor exports outside the repository.
_REPO = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
SLR_DATA = _os.environ.get("SLR_DATA", _os.path.join(_REPO, "data"))
CORPUS = os.path.join(SLR_DATA, "biblio_output", "corpus_unificado.csv")
OUT = os.path.join(SLR_DATA, "biblio_output", "screening_set.json")

csv.field_size_limit(10_000_000)


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def load_abstracts() -> dict[str, dict]:
    """Map normalized title -> {abstract, venue, volume, issue, pages}."""
    found: dict[str, dict] = {}
    for i in range(1, 6):
        path = os.path.join(SLR_DATA, f"rq{i}scopus.csv")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                key = norm(row.get("Title"))
                if not key or key in found:
                    continue
                start, end = row.get("Page start") or "", row.get("Page end") or ""
                found[key] = {
                    "abstract": (row.get("Abstract") or "").strip(),
                    "venue": (
                        row.get("Source title")
                        or row.get("Conference name")
                        or row.get("Abbreviated Source Title")
                        or ""
                    ).strip(),
                    "volume": (row.get("Volume") or "").strip(),
                    "issue": (row.get("Issue") or "").strip(),
                    "pages": f"{start}-{end}".strip("-"),
                }
    return found


def main() -> int:
    abstracts = load_abstracts()
    print(f"  abstracts available from raw exports: {len(abstracts)}")

    with open(CORPUS, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    seen: set[str] = set()
    records = []
    for row in rows:
        key = norm(row.get("Title"))
        if key in seen:  # the two dual-RQ studies appear twice
            for rec in records:
                if rec["key"] == key and row["RQ"] not in rec["rq"]:
                    rec["rq"].append(row["RQ"])
            continue
        seen.add(key)
        extra = abstracts.get(key, {})
        records.append(
            {
                "id": row.get("Article_ID"),
                "key": key,
                "title": (row.get("Title") or "").strip(),
                "authors": (row.get("Authors") or "").strip(),
                "year": (row.get("Year") or "").strip(),
                "venue": (row.get("Source title") or "").strip() or extra.get("venue", ""),
                "doi": (row.get("DOI") or "").strip(),
                "doc_type": (row.get("Document Type") or "").strip(),
                "source": (row.get("Source") or "").strip(),
                "rq": [row.get("RQ", "")],
                "author_keywords": (row.get("Author Keywords") or "").strip(),
                "index_keywords": (row.get("Index Keywords") or "").strip(),
                "abstract": extra.get("abstract", ""),
                "volume": extra.get("volume", ""),
                "issue": extra.get("issue", ""),
                "pages": extra.get("pages", ""),
            }
        )

    with_abs = sum(1 for r in records if r["abstract"])
    recovered_venue = sum(
        1 for r in records if r["venue"] and not r["doi"] == "" or r["venue"]
    )
    print(f"  distinct studies: {len(records)}")
    print(f"  with abstract:    {with_abs}")
    print(f"  with venue:       {sum(1 for r in records if r['venue'])}")
    print(f"  with volume:      {sum(1 for r in records if r['volume'])}")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=1, ensure_ascii=False)
    print(f"  written: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
