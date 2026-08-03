"""Tune a candidate query block by block against the screened corpus.

Measuring a query only by how many records it returns says nothing about
whether it returns the right ones. This script scores candidates on the two
quantities that matter: how much of the corpus the re-screening retained is
recovered, and how much of what it excluded comes back.

Only studies whose provenance is the database search count towards recall.
Studies reached by citation chasing or by the citation-index pass are not
retrievable by a database query and would depress the score unfairly.

Usage:
    bash containers/run.sh slr-update python scripts/slr-update/tune_queries.py RQ3
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import os as _os

# Resolve the corpus location without hard-coding anyone's home directory:
# the repository's own data/ directory by default, overridable for a working
# tree that keeps the raw vendor exports outside the repository.
_REPO = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
SLR_DATA = _os.environ.get("SLR_DATA", _os.path.join(_REPO, "data"))
BIBLIO = os.path.join(SLR_DATA, "biblio_output")
SCOPUS_URL = "https://api.elsevier.com/content/search/scopus"
PAGE = 25
MAX_PAGINATE = 600  # do not paginate candidates broader than this

csv.field_size_limit(10_000_000)

FILTERS = (
    "PUBYEAR > 1999 AND PUBYEAR < 2027 "
    "AND (DOCTYPE(ar) OR DOCTYPE(cp) OR DOCTYPE(re) OR DOCTYPE(ch)) "
    "AND LANGUAGE(english)"
)

API_TIGHT = (
    '"REST API" OR "RESTful API" OR "web API" OR "HTTP API" OR "API security" '
    'OR "API testing" OR "OpenAPI" OR "microservice*"'
)
API_WIDE = API_TIGHT + ' OR "web service*" OR "cloud API" OR "service composition"'

CANDIDATES = {
    "RQ3": [
        ("A: actual (demasiado ancha)", [API_WIDE,
            'vulnerabilit* OR "security flaw*" OR exploit* OR attack* OR "security defect*"',
            'cause* OR factor* OR source* OR "root cause*" OR detect* OR discover*']),
        ("B: sin detect/discover", [API_WIDE,
            'vulnerabilit* OR "security flaw*" OR exploit* OR "security defect*"',
            'cause* OR factor* OR source* OR "root cause*"']),
        ("C: B + API estrecha", [API_TIGHT,
            'vulnerabilit* OR "security flaw*" OR exploit* OR "security defect*"',
            'cause* OR factor* OR source* OR "root cause*"']),
        ("D: C + ancla de analisis", [API_TIGHT,
            'vulnerabilit* OR "security flaw*" OR exploit* OR "security defect*"',
            'cause* OR factor* OR source* OR "root cause*" OR "empirical stud*" OR analysis']),
    ],
    "RQ4": [
        ("A: actual", [API_WIDE,
            'vulnerabilit* OR "security threat*" OR attack*',
            '"mitigation strateg*" OR "security framework*" OR "defense mechanis*" '
            'OR "vulnerability management" OR "risk reduction" OR countermeasure* '
            'OR "hardening technique*" OR "secure design" OR "security control*"']),
        ("B: API estrecha", [API_TIGHT,
            'vulnerabilit* OR "security threat*" OR attack*',
            '"mitigation strateg*" OR "security framework*" OR "defense mechanis*" '
            'OR "vulnerability management" OR "risk reduction" OR countermeasure* '
            'OR "hardening technique*" OR "secure design" OR "security control*"']),
    ],
    "RQ5": [
        ("A: actual (demasiado estrecha)", [API_WIDE,
            '"security misconfiguration*" OR misconfigur* OR "insecure configuration*" '
            'OR "security configuration*" OR hardening',
            "securit* OR vulnerabilit* OR exposure* OR attack*"]),
        ("B: configuracion general + seguridad obligatoria", [API_WIDE,
            'configuration* OR misconfigur* OR hardening OR "security setting*" '
            'OR deployment* OR "access control"',
            "securit* OR vulnerabilit* OR exposure* OR attack* OR misconfigur*"]),
        ("C: B con API estrecha", [API_TIGHT,
            'configuration* OR misconfigur* OR hardening OR "security setting*" '
            'OR deployment* OR "access control"',
            "securit* OR vulnerabilit* OR exposure* OR attack* OR misconfigur*"]),
    ],
}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def build(blocks):
    return " AND ".join(f"TITLE-ABS-KEY({b})" for b in blocks) + f" AND {FILTERS}"


def call(query, key, start=0, count=1):
    params = {"query": query, "count": count, "start": start}
    req = urllib.request.Request(
        f"{SCOPUS_URL}?{urllib.parse.urlencode(params)}",
        headers={"X-ELS-APIKey": key, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        return {"__error__": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001
        return {"__error__": str(exc)}


def total_of(body):
    return int(body.get("search-results", {}).get("opensearch:totalResults") or 0)


def paginate(query, key, total):
    titles, start = set(), 0
    while start < min(total, MAX_PAGINATE):
        body = call(query, key, start=start, count=PAGE)
        if "__error__" in body:
            break
        for e in body.get("search-results", {}).get("entry", []) or []:
            if "error" not in e:
                titles.add(norm(e.get("dc:title", "")))
        start += PAGE
        time.sleep(0.35)
    return titles


def reference_sets(rq):
    v = json.load(open(os.path.join(BIBLIO, "rescreening_verdicts.json"), encoding="utf-8"))
    v = v.get("result", v)
    excl = {e["id"] for e in v["excluir"]}
    keep, drop = set(), set()
    with open(os.path.join(BIBLIO, "corpus_unificado.csv"), encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not row["RQ"].startswith(rq):
                continue
            if row["Article_ID"] in excl:
                drop.add(norm(row["Title"]))
            elif row["Source"].strip() == "Scopus":
                keep.add(norm(row["Title"]))
    return keep, drop


def main():
    rq = sys.argv[1] if len(sys.argv) > 1 else "RQ3"
    key = os.environ.get("SCOPUS_API_KEY", "").strip()
    if not key:
        print("ERROR: SCOPUS_API_KEY not set", file=sys.stderr)
        return 2
    keep, drop = reference_sets(rq)
    print(f"  {rq}: {len(keep)} retenidos via Scopus, {len(drop)} excluidos\n")

    for label, blocks in CANDIDATES.get(rq, []):
        q = build(blocks)
        total = total_of(call(q, key))
        if total > MAX_PAGINATE:
            print(f"  {label:42s} total={total:<6d} (demasiado ancha, no se pagina)")
            continue
        got = paginate(q, key, total)
        print(
            f"  {label:42s} total={total:<6d} "
            f"recall={len(got & keep)}/{len(keep):<3d} fuga={len(got & drop)}/{len(drop)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
