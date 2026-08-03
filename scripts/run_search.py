"""Execute the five search queries against Scopus and Web of Science.

Paginates each query, deduplicates on identifier and then on normalized title,
and writes one JSON file per research question.

The Web of Science Starter API allows fifty requests per day and one per
second, so pagination is budgeted and the run stops rather than spending the
day's allowance. Run probe_totals.py first to see what each query costs.

Usage:
    export SCOPUS_API_KEY=...      # https://dev.elsevier.com/
    export WOS_API_KEY=...         # https://developer.clarivate.com/

    python3 scripts/run_search.py
    python3 scripts/run_search.py --scopus-only
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = os.environ.get("SEARCH_OUT", os.path.join(REPO, "search-results"))

sys.path.insert(0, HERE)
from queries import QUERIES  # noqa: E402

SCOPUS_URL = "https://api.elsevier.com/content/search/scopus"
WOS_URL = "https://api.clarivate.com/apis/wos-starter/v1/documents"
SCOPUS_PAGE, WOS_PAGE = 25, 50
WOS_DAILY_BUDGET = 45

# The filters the review set through each interface, expressed inline so a
# programmatic run matches a manual one.
SCOPUS_FILTERS = (
    "PUBYEAR > 1999 AND PUBYEAR < 2027 "
    "AND (DOCTYPE(ar) OR DOCTYPE(cp) OR DOCTYPE(re) OR DOCTYPE(ch)) "
    "AND LANGUAGE(english)"
)
WOS_FILTERS = "PY=(2000-2026)"


def norm(text: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def fetch(url: str, params: dict, headers: dict, tries: int = 3):
    for attempt in range(tries):
        request = urllib.request.Request(
            f"{url}?{urllib.parse.urlencode(params)}", headers=headers
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                body = json.loads(response.read().decode("utf-8", errors="replace"))
                return body, dict(response.headers)
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
    return {"__error__": "retries exhausted"}, {}


def scopus_search(query: str, key: str) -> list[dict]:
    records, start = [], 0
    while True:
        body, _ = fetch(
            SCOPUS_URL,
            {"query": f"{query} AND {SCOPUS_FILTERS}",
             "count": SCOPUS_PAGE, "start": start},
            {"X-ELS-APIKey": key, "Accept": "application/json"},
        )
        if "__error__" in body:
            print(f"      scopus stopped at start={start}: {body['__error__']}", flush=True)
            break
        results = body.get("search-results", {})
        total = int(results.get("opensearch:totalResults") or 0)
        for entry in results.get("entry", []) or []:
            if "error" in entry:
                continue
            records.append({
                "title": entry.get("dc:title", ""),
                "authors": entry.get("dc:creator", ""),
                "year": (entry.get("prism:coverDate") or "")[:4],
                "venue": entry.get("prism:publicationName", ""),
                "doi": (entry.get("prism:doi") or "").lower(),
                "doc_type": entry.get("subtypeDescription", ""),
                "cited_by": entry.get("citedby-count", ""),
                "id": entry.get("eid", ""),
                "db": "scopus",
            })
        start += SCOPUS_PAGE
        if start >= total or not results.get("entry"):
            break
        time.sleep(0.4)
    return records


def wos_search(query: str, key: str, budget: list[int]) -> list[dict]:
    records, page = [], 1
    while True:
        if budget[0] <= 1:
            print("      wos daily budget exhausted, stopping", flush=True)
            break
        body, headers = fetch(
            WOS_URL,
            {"q": f"{query} AND {WOS_FILTERS}", "limit": WOS_PAGE,
             "page": page, "db": "WOS"},
            {"X-ApiKey": key, "Accept": "application/json"},
        )
        budget[0] = int(headers.get("x-ratelimit-remaining-day") or budget[0] - 1)
        if "__error__" in body:
            print(f"      wos stopped at page={page}: {body['__error__']}", flush=True)
            break
        total = body.get("metadata", {}).get("total", 0)
        for hit in body.get("hits", []) or []:
            source = hit.get("source", {}) or {}
            names = (hit.get("names", {}) or {}).get("authors", []) or []
            records.append({
                "title": hit.get("title", ""),
                "authors": "; ".join(a.get("displayName", "") for a in names[:8]),
                "year": str(source.get("publishYear", "")),
                "venue": source.get("sourceTitle", ""),
                "doi": ((hit.get("identifiers", {}) or {}).get("doi") or "").lower(),
                "doc_type": "; ".join(hit.get("types", []) or []),
                "cited_by": "",
                "id": hit.get("uid", ""),
                "db": "wos",
            })
        if page * WOS_PAGE >= total or not body.get("hits"):
            break
        page += 1
        time.sleep(1.4)
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scopus-only", action="store_true")
    parser.add_argument("--wos-only", action="store_true")
    args = parser.parse_args()

    scopus_key = os.environ.get("SCOPUS_API_KEY", "").strip()
    wos_key = os.environ.get("WOS_API_KEY", "").strip()
    if not scopus_key and not wos_key:
        print("ERROR: set SCOPUS_API_KEY, WOS_API_KEY, or both", file=sys.stderr)
        return 2

    os.makedirs(OUT_DIR, exist_ok=True)
    wos_budget = [WOS_DAILY_BUDGET]
    summary = []

    for entry in QUERIES:
        rq = entry["rq"]
        print(f"  {rq}", flush=True)
        records = []
        if not args.wos_only and scopus_key:
            found = scopus_search(entry["scopus"], scopus_key)
            print(f"      scopus: {len(found)}", flush=True)
            records += found
        if not args.scopus_only and wos_key:
            found = wos_search(entry["wos"], wos_key, wos_budget)
            print(f"      wos:    {len(found)}  (quota left {wos_budget[0]})", flush=True)
            records += found

        seen, unique = set(), []
        for record in records:
            key = record["doi"] or norm(record["title"])
            if key and key not in seen:
                seen.add(key)
                unique.append(record)

        path = os.path.join(OUT_DIR, f"{rq.lower()}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(unique, fh, indent=1, ensure_ascii=False)
        summary.append({"rq": rq, "retrieved": len(records), "unique": len(unique)})
        print(f"      {len(unique)} unique -> {os.path.basename(path)}", flush=True)

    with open(os.path.join(OUT_DIR, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print()
    print(f"  {'RQ':6s} {'retrieved':>10s} {'unique':>8s}")
    for row in summary:
        print(f"  {row['rq']:6s} {row['retrieved']:>10d} {row['unique']:>8d}")
    print(f"\n  written to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
