#!/usr/bin/env python3
"""Rebuild the author-level aggregates from the corpus.

Derives authors_long.csv, autores_mas_productivos.csv and coautoria_edge_list.csv
from the corpus, so that every author-level figure covers the same records as
the rest of the bibliometric analysis.

Author strings are taken from the "Authors" field and split on ";". Records
without an author field are skipped and reported. Co-authorship edges are
undirected and counted once per shared article, with the pair ordered so that
the same collaboration always produces the same row.

Run:  python3 rebuild_author_aggregates.py
"""
from __future__ import annotations

import shutil
from collections import Counter
from itertools import combinations
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
BIBLIO = BASE.parent / "data"   # the deposited corpus and aggregates


def backup(path: Path) -> None:
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak.20260802"))


def split_authors(value) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    return [a.strip() for a in value.split(";") if a.strip()]


def author_key(name: str) -> tuple[str, str] | None:
    """Normalize an author string to (lastname, given name), both lowercased.

    Two formats coexist in the corpus, one per search pass:
      "S., Salva, Sebastien"   Scopus export, leading initial
      "Arcuri, Andrea"         the later passes
    Keying on the pair merges the two surface forms of one person. The key
    deliberately uses the FULL given name rather than its initial: keying on
    the initial merges distinct researchers who share a surname and an
    initial, and this corpus contains such a pair (Zhang Man and Zhang
    Mengjie), which a first pass over the data silently collapsed into one.

    Returns None for strings that are not names, such as the BibTeX
    "and others" artifact.
    """
    parts = [p.strip() for p in name.split(",") if p.strip()]
    if not parts:
        return None
    if len(parts) >= 3 and parts[0].endswith(".") and len(parts[0]) <= 3:
        last, first = parts[1], parts[2]
    elif len(parts) >= 2:
        last, first = parts[0], parts[1]
    else:
        last, first = parts[0], ""
    first = first.replace(" and others", "").strip()
    if not last or last.lower() in {"and others", "others", "et al."}:
        return None
    return (last.lower(), first.lower())


def main() -> int:
    corpus = pd.read_csv(BIBLIO / "corpus.csv").rename(
        columns={"authors": "Authors", "rq": "RQ", "id": "Article_ID"}
    )

    long_rows: list[dict] = []
    per_article: list[list[str]] = []
    missing = 0

    for _, row in corpus.iterrows():
        authors = split_authors(row.get("Authors"))
        if not authors:
            missing += 1
            continue
        per_article.append(authors)
        for a in authors:
            long_rows.append({
                "Article_ID": row["Article_ID"],
                "Author": a,
                "RQ": row["RQ"],
            })

    long_df = pd.DataFrame(long_rows)
    backup(BIBLIO / "authors_long.csv")
    long_df.to_csv(BIBLIO / "authors_long.csv", index=False)

    # Productivity counts distinct articles, not authorship rows, so that a
    # study assigned to two research questions does not inflate its authors.
    long_df["Key"] = long_df["Author"].map(author_key)
    long_df = long_df[long_df["Key"].notna()].copy()
    uniq = long_df.drop_duplicates(subset=["Article_ID", "Key"])
    counts = uniq.groupby("Key").size()
    # display the longest surface form seen for each key
    display = (long_df.groupby("Key")["Author"]
                      .agg(lambda s: max(s, key=len)))
    prod = (pd.DataFrame({"Author": display, "N_articulos": counts})
              .sort_values("N_articulos", ascending=False)
              .reset_index(drop=True))
    backup(BIBLIO / "autores_mas_productivos.csv")
    prod.to_csv(BIBLIO / "autores_mas_productivos.csv", index=False)

    # One canonical display name per person, chosen globally as the longest
    # surface form, so that the two spellings of a name are ONE node in the
    # co-authorship graph rather than two.
    canonical: dict = {}
    for _, row in corpus.iterrows():
        for name in split_authors(row.get("Authors")):
            k = author_key(name)
            if k is None:
                continue
            if k not in canonical or len(name) > len(canonical[k]):
                canonical[k] = name

    edges: Counter = Counter()
    seen_articles: set = set()
    for _, row in corpus.iterrows():
        if row["Article_ID"] in seen_articles:
            continue
        seen_articles.add(row["Article_ID"])
        keys = set()
        for name in split_authors(row.get("Authors")):
            k = author_key(name)
            if k is not None:
                keys.add(k)
        authors = sorted(canonical[k] for k in keys)
        for a, b in combinations(authors, 2):
            edges[(a, b)] += 1

    edge_df = pd.DataFrame(
        [{"Author1": a, "Author2": b, "Weight": w} for (a, b), w in edges.items()]
    ).sort_values(["Weight", "Author1"], ascending=[False, True])
    backup(BIBLIO / "coautoria_edge_list.csv")
    edge_df.to_csv(BIBLIO / "coautoria_edge_list.csv", index=False)

    print(f"records                 {len(corpus)}")
    print(f"records without authors {missing}")
    print(f"authorship rows         {len(long_df)}")
    print(f"distinct authors        {len(prod)}")
    print(f"co-authorship edges     {len(edge_df)}")
    print("\ntop 10 authors:")
    for _, r in prod.head(10).iterrows():
        print(f"  {r['N_articulos']:>2}  {r['Author']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
