"""Measure how large a full re-run of the five SLR queries would be.

Costs one request per query per database (10 total). The Web of Science
Starter API allows 50 requests per day and one per second, so knowing the
result-set sizes before paginating is the difference between a planned
re-run and an exhausted daily quota.

Usage:
    bash containers/run.sh slr-update python scripts/slr-update/probe_totals.py
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queries import QUERIES  # noqa: E402

SCOPUS_URL = "https://api.elsevier.com/content/search/scopus"
WOS_URL = "https://api.clarivate.com/apis/wos-starter/v1/documents"

SCOPUS_PAGE = 25   # records per Scopus page (API maximum for the standard key)
WOS_PAGE = 50      # records per WoS Starter page (API maximum)

# The search window declared in the review.
YEAR_FROM, YEAR_TO = 2000, 2026


def fetch(url: str, params: dict, headers: dict, timeout: int = 60):
    """GET a JSON endpoint. Returns (status, parsed_body_or_text, headers)."""
    full = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(full, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(body), dict(resp.headers)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass
        return exc.code, body, dict(exc.headers)
    except Exception as exc:  # noqa: BLE001
        return 0, {"error": str(exc)}, {}


def scopus_total(query: str, key: str):
    params = {
        "query": f"{query} AND PUBYEAR > {YEAR_FROM - 1} AND PUBYEAR < {YEAR_TO + 1}",
        "count": 1,
    }
    status, body, _ = fetch(
        SCOPUS_URL, params, {"X-ELS-APIKey": key, "Accept": "application/json"}
    )
    if status != 200:
        return None, f"HTTP {status}: {str(body)[:120]}"
    total = body.get("search-results", {}).get("opensearch:totalResults")
    return int(total) if total is not None else None, None


def wos_total(query: str, key: str):
    params = {
        "q": f"{query} AND PY=({YEAR_FROM}-{YEAR_TO})",
        "limit": 1,
        "db": "WOS",
    }
    status, body, hdrs = fetch(
        WOS_URL, params, {"X-ApiKey": key, "Accept": "application/json"}
    )
    quota = hdrs.get("x-ratelimit-remaining-day")
    if status != 200:
        return None, f"HTTP {status}: {str(body)[:120]}", quota
    return body.get("metadata", {}).get("total"), None, quota


def pages(total: int, per_page: int) -> int:
    return (total + per_page - 1) // per_page if total else 0


def main() -> int:
    scopus_key = os.environ.get("SCOPUS_API_KEY", "").strip()
    wos_key = os.environ.get("WOS_API_KEY", "").strip()
    if not scopus_key or not wos_key:
        print("ERROR: SCOPUS_API_KEY and WOS_API_KEY must both be set", file=sys.stderr)
        return 2

    rows = []
    quota_left = None

    for q in QUERIES:
        rq = q["rq"]

        s_total, s_err = scopus_total(q["scopus"], scopus_key)
        time.sleep(0.5)

        w_total, w_err, quota_left = wos_total(q["wos"], wos_key)
        time.sleep(1.5)  # WoS Starter allows one request per second

        rows.append(
            {
                "rq": rq,
                "scopus_total": s_total,
                "scopus_error": s_err,
                "wos_total": w_total,
                "wos_error": w_err,
            }
        )
        print(
            f"  {rq}  scopus={s_total if s_total is not None else s_err}"
            f"   wos={w_total if w_total is not None else w_err}",
            flush=True,
        )

    print()
    s_sum = sum(r["scopus_total"] or 0 for r in rows)
    w_sum = sum(r["wos_total"] or 0 for r in rows)
    s_pages = sum(pages(r["scopus_total"] or 0, SCOPUS_PAGE) for r in rows)
    w_pages = sum(pages(r["wos_total"] or 0, WOS_PAGE) for r in rows)

    print(f"  Scopus: {s_sum} records -> {s_pages} requests to paginate")
    print(f"  WoS:    {w_sum} records -> {w_pages} requests to paginate")
    print(f"  WoS daily quota remaining after this probe: {quota_left}")
    if quota_left is not None and w_pages > int(quota_left):
        print(
            f"  WARNING: paginating WoS needs {w_pages} requests but only "
            f"{quota_left} remain today; the re-run must span more than one day."
        )

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_totals.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "year_from": YEAR_FROM,
                "year_to": YEAR_TO,
                "rows": rows,
                "scopus_records": s_sum,
                "wos_records": w_sum,
                "scopus_requests": s_pages,
                "wos_requests": w_pages,
                "wos_quota_remaining": quota_left,
            },
            fh,
            indent=2,
        )
    print(f"  written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
