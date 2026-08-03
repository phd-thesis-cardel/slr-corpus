"""Write the search strings out as plain files, one per question per database.

The strings live in a Python module because the pipeline executes them from
there. A reader who wants to paste a query into the Scopus or Web of Science
interface should not have to read Python to find it.

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

FIELD = {"Scopus": "TITLE-ABS-KEY", "Web of Science": "TS"}

HEADER = """\
# {rq} -- {db}
#
# {description}
#
# The filters on publication year (2000 to 2026), document type (article,
# conference paper, review, book chapter) and language (English) are set
# through the {db} interface and are not part of the string below.
#
# Paste the block into the {field} field. Line breaks are for reading only;
# the interface treats the string as one line.

"""


def wrap(query: str, width: int = 88) -> str:
    return "\n".join(
        textwrap.wrap(" ".join(query.split()), width=width, break_long_words=False)
    )


def write(path: str, body: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


def main() -> int:
    bundle = []
    written = 0
    for entry in QUERIES:
        for db, key in (("Scopus", "scopus"), ("Web of Science", "wos")):
            body = HEADER.format(
                rq=entry["rq"], db=db, description=entry["description"],
                field=FIELD[db],
            ) + wrap(entry[key]) + "\n"
            write(os.path.join(OUT, f"{entry['rq'].lower()}-{key}.txt"), body)
            written += 1
        bundle.append({
            "rq": entry["rq"],
            "description": entry["description"],
            "scopus": " ".join(entry["scopus"].split()),
            "wos": " ".join(entry["wos"].split()),
        })

    write(os.path.join(OUT, "queries.json"),
          json.dumps(bundle, indent=2, ensure_ascii=False) + "\n")
    print(f"  {written} query files -> {OUT}")
    print(f"  machine-readable     -> {OUT}/queries.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
