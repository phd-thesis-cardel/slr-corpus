"""Turn the re-screening verdicts into a reviewable evidence document.

Every proposed exclusion is listed with the verbatim abstract fragment the
adjudication rested on, so the decision can be checked study by study rather
than accepted wholesale. Rescued studies are listed separately with the
argument that saved them.

Usage:
    python3 scripts/slr-update/export_screening_evidence.py <workflow-output.json> <out.md>
"""

from __future__ import annotations

import csv
import json
import os
import sys
from collections import defaultdict

import os as _os

# Resolve the corpus location without hard-coding anyone's home directory:
# the repository's own data/ directory by default, overridable for a working
# tree that keeps the raw vendor exports outside the repository.
_REPO = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
SLR_DATA = _os.environ.get("SLR_DATA", _os.path.join(_REPO, "data"))
CORPUS = _os.path.join(SLR_DATA, "corpus.csv")


def load_corpus() -> dict[str, dict]:
    with open(CORPUS, encoding="utf-8") as fh:
        return {r["Article_ID"]: r for r in csv.DictReader(fh)}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    raw = json.load(open(sys.argv[1], encoding="utf-8"))
    result = raw.get("result", raw)
    corpus = load_corpus()

    excluir = result["excluir"]
    rescatados = result["rescatados"]

    by_rq: dict[str, list] = defaultdict(list)
    for e in excluir:
        row = corpus.get(e["id"], {})
        rq = (row.get("RQ") or "sin RQ").split(":")[0].strip()
        by_rq[rq].append((e, row))

    lines = [
        "---",
        "title: Evidence for the re-screening of the systematic review corpus",
        "author: Carlos A. Delgado S.",
        "date: 2026-08-03",
        "version: 1.0",
        "status: review",
        "tags: [slr, prisma, screening, corpus]",
        "---",
        "",
        "# Re-screening evidence",
        "",
        "Every study in the corpus was judged again against the inclusion and",
        "exclusion criteria declared in the review methodology, in particular the",
        "two exclusion clauses that read *Publications not directly related to",
        "RESTful API security or mutation testing* and *Articles focusing on",
        "non-RESTful API security or unrelated mutation testing domains*.",
        "",
        "Each proposed exclusion was then given to an independent adjudicator",
        "instructed to rescue it if any honest reading placed the study inside the",
        "broad bibliometric scope, which admits adjacent work on web services,",
        "fault injection and stateful fuzzing. Studies that survived that step are",
        "listed in the second section and remain in the corpus.",
        "",
        f"- Studies judged: **{result['total_juzgados']}**",
        f"- Exclusions upheld: **{len(excluir)}**",
        f"- Proposed exclusions rescued: **{len(rescatados)}**",
        f"- Corpus after re-screening: **{result['total_juzgados'] - len(excluir)}**",
        "",
        "The dominant cause is homonymy. The term *mutation operator* carries a",
        "distinct technical meaning in evolutionary computation, where it names a",
        "genetic operator, and *mutation* carries a third meaning in molecular",
        "biology. Neither sense is the one this review is about.",
        "",
        "## Exclusions upheld",
        "",
    ]

    for rq in sorted(by_rq):
        lines.append(f"### {rq} ({len(by_rq[rq])} studies)")
        lines.append("")
        for e, row in by_rq[rq]:
            title = e["title"]
            year = row.get("Year", "")
            venue = row.get("Source title", "") or "(no venue field)"
            doi = row.get("DOI", "") or "(no DOI)"
            lines.append(f"**{title}**  ")
            lines.append(f"`ID {e['id']}` · {year} · {venue} · {doi}")
            lines.append("")
            lines.append(f"*Reason.* {e['reason']}")
            lines.append("")
            if e.get("evidence"):
                ev = e["evidence"].strip().strip('"')
                lines.append(f"> {ev}")
                lines.append("")

    lines.append("## Proposed exclusions that were rescued")
    lines.append("")
    lines.append("These studies were flagged in the first pass and are retained.")
    lines.append("")
    for r in rescatados:
        row = corpus.get(r["id"], {})
        lines.append(f"**{r['title']}**  ")
        lines.append(f"`ID {r['id']}` · {row.get('Year','')} · {row.get('Source title','') or '(no venue field)'}")
        lines.append("")
        lines.append(f"*Retained because.* {r['argument']}")
        lines.append("")

    out = sys.argv[2]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  written: {out}  ({len(excluir)} exclusions, {len(rescatados)} rescues)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
