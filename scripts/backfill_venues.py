"""Fill the empty venue cells of the corpus from the raw database exports.

Twenty-seven included studies carry no publication venue. The gap is not one of
data but of consolidation: the Scopus exports record conference venues under
"Conference name" and an abbreviated form under "Abbreviated Source Title",
and the script that built the unified corpus only ever read "Source title". A
study identified by author and year alone is not retrievable, which is what
item 17 of PRISMA asks a corpus table to enable, so the gap is worth closing at
the source rather than annotating downstream.

Records still empty after this pass are reported by title so the remainder can
be resolved by hand or left declared as missing.

Usage:
    bash containers/run.sh biblio python slr-data/backfill_venues.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
CORPUS = BASE / "biblio_output" / "corpus_unificado.csv"

csv.field_size_limit(10_000_000)

VENUE_COLUMNS = ("Source title", "Conference name", "Abbreviated Source Title")


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def harvest() -> dict[str, str]:
    """Map normalized title -> venue, from every raw Scopus export."""
    found: dict[str, str] = {}
    for path in sorted(BASE.glob("rq*scopus.csv")):
        with open(path, encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                key = norm(row.get("Title"))
                if not key or found.get(key):
                    continue
                for col in VENUE_COLUMNS:
                    value = (row.get(col) or "").strip()
                    if value:
                        found[key] = value
                        break
    return found


def _crossref(url: str):
    req = urllib.request.Request(
        url, headers={"User-Agent": "slr-backfill (mailto:cardel87@gmail.com)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))["message"]
    except Exception:  # noqa: BLE001
        return None


def _venue_of(msg: dict) -> str:
    for value in (msg.get("container-title") or []):
        if value:
            return value
    return (msg.get("event") or {}).get("name", "") or ""


def crossref_venue(doi: str, title: str) -> tuple[str, str]:
    """Return (venue, doi). The DOI comes back corrected if it did not resolve."""
    msg = _crossref(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
    if msg:
        return _venue_of(msg), doi
    if not title.strip():
        return "", ""
    query = urllib.parse.urlencode(
        {"query.bibliographic": title[:200], "rows": 1, "mailto": "cardel87@gmail.com"}
    )
    msg = _crossref(f"https://api.crossref.org/works?{query}")
    items = (msg or {}).get("items") or []
    if not items:
        return "", ""
    found = items[0]
    # Guard against a loose match: the retrieved title must agree.
    if norm((found.get("title") or [""])[0])[:40] != norm(title)[:40]:
        return "", ""
    time.sleep(0.3)
    return _venue_of(found), found.get("DOI", "")


def main() -> int:
    venues = harvest()
    print(f"  venues available in the raw exports: {len(venues)}")

    with open(CORPUS, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
        fields = list(rows[0].keys())

    filled = 0
    for row in rows:
        if (row.get("Source title") or "").strip():
            continue
        venue = venues.get(norm(row.get("Title")))
        if venue:
            row["Source title"] = venue
            filled += 1

    # Second pass: whatever the exports could not supply, ask the DOI registry.
    # One record carries a DOI truncated on import (10.5220/000597080), which
    # resolves to nothing; it is repaired by a title search before the lookup.
    repaired = 0
    for row in rows:
        if (row.get("Source title") or "").strip():
            continue
        doi = (row.get("DOI") or "").strip()
        if not doi:
            continue
        venue, better_doi = crossref_venue(doi, row.get("Title", ""))
        if better_doi and better_doi.lower() != doi.lower():
            row["DOI"] = better_doi
            repaired += 1
        if venue:
            row["Source title"] = venue
            filled += 1
    if repaired:
        print(f"  DOIs repaired via title search: {repaired}")

    still_empty = [r for r in rows if not (r.get("Source title") or "").strip()]

    backup = CORPUS.with_suffix(".csv.bak.prebackfill")
    if not backup.exists():
        backup.write_text(CORPUS.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  backup: {backup.name}")

    with open(CORPUS, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  venue cells filled: {filled}")
    print(f"  still empty:        {len(still_empty)}")
    for row in still_empty:
        doi = (row.get("DOI") or "").strip() or "no DOI"
        print(f"    - [{doi}] {(row.get('Title') or '')[:66]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
