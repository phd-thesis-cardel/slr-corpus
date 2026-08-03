"""Execute the corrected searches and measure them against the screened corpus.

For every research question the script paginates Scopus and Web of Science,
stores the records, and then reports two quantities that decide whether the
corrected query is an improvement rather than merely a change:

  recall  -- how many of the studies the re-screening retained are retrieved
  leakage -- how many of the studies the re-screening excluded come back

A corrected query is only defensible if recall holds and leakage falls.

The Web of Science Starter API allows fifty requests per day and one per
second, so pagination is budgeted and the script stops rather than burning the
daily allowance.

Usage:
    bash containers/run.sh slr-update python scripts/slr-update/rerun_search.py
    bash containers/run.sh slr-update python scripts/slr-update/rerun_search.py --scopus-only
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queries_v2 import QUERIES_V2  # noqa: E402

import os as _os

# Resolve the corpus location without hard-coding anyone's home directory:
# the repository's own data/ directory by default, overridable for a working
# tree that keeps the raw vendor exports outside the repository.
_REPO = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
SLR_DATA = _os.environ.get("SLR_DATA", _os.path.join(_REPO, "data"))
BIBLIO = os.path.join(SLR_DATA, "biblio_output")
CORPUS = os.path.join(BIBLIO, "corpus_unificado.csv")
VERDICTS = os.path.join(BIBLIO, "rescreening_verdicts.json")
OUT_DIR = os.path.join(SLR_DATA, "rerun_2026_08")

SCOPUS_URL = "https://api.elsevier.com/content/search/scopus"
WOS_URL = "https://api.clarivate.com/apis/wos-starter/v1/documents"
SCOPUS_PAGE, WOS_PAGE = 25, 50

csv.field_size_limit(10_000_000)


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def fetch(url: str, params: dict, headers: dict, tries: int = 3):
    for attempt in range(tries):
        full = f"{url}?{urllib.parse.urlencode(params)}"
        try:
            req = urllib.request.Request(full, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace")), dict(resp.headers)
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503) and attempt < tries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            return {"__error__": f"HTTP {exc.code}"}, dict(exc.headers or {})
        except Exception as exc:  # noqa: BLE001
            if attempt < tries - 1:
                time.sleep(3)
                continue
            return {"__error__": str(exc)}, {}
    return {"__error__": "exhausted"}, {}


def scopus_search(query: str, key: str) -> list[dict]:
    out, start = [], 0
    while True:
        body, _ = fetch(
            SCOPUS_URL,
            {"query": query, "count": SCOPUS_PAGE, "start": start},
            {"X-ELS-APIKey": key, "Accept": "application/json"},
        )
        if "__error__" in body:
            print(f"      scopus error at start={start}: {body['__error__']}", flush=True)
            break
        res = body.get("search-results", {})
        total = int(res.get("opensearch:totalResults") or 0)
        for e in res.get("entry", []) or []:
            if "error" in e:
                continue
            out.append(
                {
                    "title": e.get("dc:title", ""),
                    "authors": e.get("dc:creator", ""),
                    "year": (e.get("prism:coverDate") or "")[:4],
                    "venue": e.get("prism:publicationName", ""),
                    "doi": (e.get("prism:doi") or "").lower(),
                    "doc_type": e.get("subtypeDescription", ""),
                    "cited_by": e.get("citedby-count", ""),
                    "eid": e.get("eid", ""),
                    "db": "scopus",
                }
            )
        start += SCOPUS_PAGE
        if start >= total or not res.get("entry"):
            break
        time.sleep(0.4)
    return out


def wos_search(query: str, key: str, budget: list[int]) -> list[dict]:
    out, page = [], 1
    while True:
        if budget[0] <= 1:
            print("      wos budget exhausted, stopping pagination", flush=True)
            break
        body, hdrs = fetch(
            WOS_URL,
            {"q": query, "limit": WOS_PAGE, "page": page, "db": "WOS"},
            {"X-ApiKey": key, "Accept": "application/json"},
        )
        budget[0] = int(hdrs.get("x-ratelimit-remaining-day") or budget[0] - 1)
        if "__error__" in body:
            print(f"      wos error at page={page}: {body['__error__']}", flush=True)
            break
        total = body.get("metadata", {}).get("total", 0)
        for h in body.get("hits", []) or []:
            src = h.get("source", {}) or {}
            ids = h.get("identifiers", {}) or {}
            names = (h.get("names", {}) or {}).get("authors", []) or []
            out.append(
                {
                    "title": h.get("title", ""),
                    "authors": "; ".join(a.get("displayName", "") for a in names[:8]),
                    "year": str(src.get("publishYear", "")),
                    "venue": src.get("sourceTitle", ""),
                    "doi": (ids.get("doi") or "").lower(),
                    "doc_type": "; ".join(h.get("types", []) or []),
                    "cited_by": "",
                    "eid": h.get("uid", ""),
                    "db": "wos",
                }
            )
        if page * WOS_PAGE >= total or not body.get("hits"):
            break
        page += 1
        time.sleep(1.4)
    return out


def load_reference_sets():
    """Return (retained_titles, excluded_titles) from the re-screening."""
    verdicts = json.load(open(VERDICTS, encoding="utf-8"))
    verdicts = verdicts.get("result", verdicts)
    excluded_ids = {e["id"] for e in verdicts["excluir"]}
    retained, excluded = {}, {}
    with open(CORPUS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rq = row["RQ"].split(":")[0].strip()
            target = excluded if row["Article_ID"] in excluded_ids else retained
            target.setdefault(rq, set()).add(norm(row["Title"]))
    return retained, excluded


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scopus-only", action="store_true")
    ap.add_argument("--wos-only", action="store_true")
    args = ap.parse_args()

    scopus_key = os.environ.get("SCOPUS_API_KEY", "").strip()
    wos_key = os.environ.get("WOS_API_KEY", "").strip()
    os.makedirs(OUT_DIR, exist_ok=True)
    retained, excluded = load_reference_sets()
    wos_budget = [45]

    summary = []
    for q in QUERIES_V2:
        rq = q["rq"]
        print(f"  {rq}", flush=True)
        records = []
        if not args.wos_only and scopus_key:
            s = scopus_search(q["scopus"], scopus_key)
            print(f"      scopus: {len(s)}", flush=True)
            records += s
        if not args.scopus_only and wos_key:
            w = wos_search(q["wos"], wos_key, wos_budget)
            print(f"      wos:    {len(w)}  (quota left {wos_budget[0]})", flush=True)
            records += w

        seen, uniq = set(), []
        for r in records:
            k = r["doi"] or norm(r["title"])
            if k and k not in seen:
                seen.add(k)
                uniq.append(r)

        titles = {norm(r["title"]) for r in uniq}
        keep, drop = retained.get(rq, set()), excluded.get(rq, set())
        recall = len(titles & keep)
        leak = len(titles & drop)
        summary.append(
            {
                "rq": rq,
                "retrieved": len(uniq),
                "retained_in_corpus": len(keep),
                "recall_hits": recall,
                "excluded_in_corpus": len(drop),
                "leakage_hits": leak,
            }
        )
        print(
            f"      unicos {len(uniq)} | recupera {recall}/{len(keep)} retenidos "
            f"| refiltra {leak}/{len(drop)} excluidos",
            flush=True,
        )

        with open(os.path.join(OUT_DIR, f"{rq.lower()}_v2.json"), "w", encoding="utf-8") as fh:
            json.dump(uniq, fh, indent=1, ensure_ascii=False)

    with open(os.path.join(OUT_DIR, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print()
    print(f"  {'RQ':5s} {'traidos':>8s} {'recall':>12s} {'fuga':>12s}")
    for s in summary:
        print(
            f"  {s['rq']:5s} {s['retrieved']:>8d} "
            f"{s['recall_hits']:>5d}/{s['retained_in_corpus']:<6d} "
            f"{s['leakage_hits']:>5d}/{s['excluded_in_corpus']:<6d}"
        )
    print(f"\n  escrito en {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
