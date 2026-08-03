"""Write the search strings out as plain files, one per question per database.

The strings live in two Python modules because the pipeline executes them from
there. A reader who wants to paste a query into the Scopus or Web of Science
interface should not have to read Python to find it, so this script mirrors both
modules into `queries/` as text files and as one JSON document.

Both forms are exported. `published/` holds the strings as they appear in the
review; `corrected/` holds the strings an update should use, with the homonymy
of *mutation* anchored on software testing and the interface block widened to
the service vocabulary the corpus contains.

Usage:
    python3 scripts/export_queries.py
"""

from __future__ import annotations

import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "queries")

sys.path.insert(0, HERE)
from queries import QUERIES  # noqa: E402
from queries_v2 import QUERIES_V2  # noqa: E402

HEADER = """\
# {rq} -- {db}
#
# {description}
#
# Form: {form}
{extra}#
# Paste the block below into the {field} field of {db}. Line breaks are for
# reading only; the interface treats the string as one line.

"""

FIELD = {"Scopus": "TITLE-ABS-KEY", "Web of Science": "TS"}


def wrap(query: str) -> str:
    """Break a long query at operator boundaries so it stays readable."""
    text = " ".join(query.split())
    for op in (" AND ", " OR "):
        text = text.replace(op, op.strip().join(("\n", " ")) if op == " AND " else op)
    return "\n".join(textwrap.wrap(text, width=88, break_long_words=False))


def write(path: str, body: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


def main() -> int:
    bundle = {"published": [], "corrected": []}
    written = 0

    for entry in QUERIES:
        for db, key in (("Scopus", "scopus"), ("Web of Science", "wos")):
            body = HEADER.format(
                rq=entry["rq"], db=db, description=entry["description"],
                form="as published with the review", extra="", field=FIELD[db],
            ) + wrap(entry[key]) + "\n"
            write(os.path.join(OUT, "published", f"{entry['rq'].lower()}-{key}.txt"), body)
            written += 1
        bundle["published"].append({
            "rq": entry["rq"], "description": entry["description"],
            "scopus": " ".join(entry["scopus"].split()),
            "wos": " ".join(entry["wos"].split()),
        })

    for entry in QUERIES_V2:
        for db, key in (("Scopus", "scopus"), ("Web of Science", "wos")):
            body = HEADER.format(
                rq=entry["rq"], db=db, description=entry["description"],
                form="corrected after the 2026-08-03 audit",
                extra=f"# Change: {entry['change']}\n", field=FIELD[db],
            ) + wrap(entry[key]) + "\n"
            write(os.path.join(OUT, "corrected", f"{entry['rq'].lower()}-{key}.txt"), body)
            written += 1
        bundle["corrected"].append({
            "rq": entry["rq"], "description": entry["description"],
            "change": entry["change"],
            "scopus": " ".join(entry["scopus"].split()),
            "wos": " ".join(entry["wos"].split()),
        })

    write(os.path.join(OUT, "queries.json"), json.dumps(bundle, indent=2, ensure_ascii=False) + "\n")
    print(f"  {written} query files -> {OUT}/published and {OUT}/corrected")
    print(f"  machine-readable bundle -> {OUT}/queries.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
