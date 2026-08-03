#!/usr/bin/env python3
"""
Targeted search update of the SLR corpus, August 2026.

Adds the records retained by the August 2026 update sweep as a third
identification stream (alongside the Scopus and Web of Science database
queries), then re-derives every aggregate CSV that feeds the bibliometric
figures of the thesis chapter and the SLR paper.

Provenance of the added records: literature sweep over the scite index
(2026-08-02), screened against the same inclusion and exclusion criteria as
the original review. 64 records were surfaced by the update queries and one
further record (Bartocci et al., 2023) came from citation chasing on those
records; 65 were screened and 15 retained.

Run:  python3 update_2026_08.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
BIBLIO = BASE / "biblio_output"
CONSOLIDATED = BASE / "consolidated"

STREAM = "Search update 2026-08"

# ---------------------------------------------------------------------------
# Records retained by the August 2026 update sweep.
#
# "Cited by" holds the citing-publication count reported by the index at
# sweep time. The 2026 records are too recent to have accrued citations;
# Bartocci et al. (2023) carries 10.
#
# Author-supplied and index keywords are left empty: these records were not
# retrieved through a Scopus/Web of Science export and therefore carry no
# normalized keyword metadata. The keyword figure is computed over the
# records that do carry it, which the chapter and the paper state explicitly.
# ---------------------------------------------------------------------------
UPDATE_RECORDS = [
    # ---------------------------- RQ1 --------------------------------------
    dict(
        Authors="Ö., Şahin, Ömür; M., Zhang, Man; A., Arcuri, Andrea",
        Title="Enhancing REST API Fuzzing with Access Policy Violation Checks and Injection Attacks",
        Year=2026, Source_title="arXiv", Document_Type="Preprint", Cited_by=0,
        DOI="10.48550/arXiv.2604.00702", RQ="RQ1: Mutation operators",
    ),
    dict(
        Authors="B., Wang, Bo; M., Chen, Mingda; M., Deng, Ming; Y., Lin, Youfang",
        Title="A Comprehensive Study on Large Language Models for Mutation Testing",
        Year=2026, Source_title="ACM Transactions on Software Engineering and Methodology",
        Document_Type="Article", Cited_by=0,
        DOI="10.1145/3805038", RQ="RQ1: Mutation operators",
    ),
    dict(
        Authors="S., Alimadadi, Saba; G., Gharachorlu, Golnaz",
        Title="Hybrid Fault-Driven Mutation Testing for Python",
        Year=2026, Source_title="arXiv", Document_Type="Preprint", Cited_by=0,
        DOI="10.48550/arXiv.2601.19088", RQ="RQ1: Mutation operators",
    ),
    dict(
        Authors="L., Kogler, Leon; S., Hangler, Stefan; M., Ehrhart, Maximilian",
        Title="RESTestBench: A Benchmark for Evaluating the Effectiveness of LLM-Generated REST API Test Cases from NL Requirements",
        Year=2026, Source_title="arXiv", Document_Type="Preprint", Cited_by=0,
        DOI="10.48550/arXiv.2604.25862", RQ="RQ1: Mutation operators",
    ),
    dict(
        Authors="E., Bartocci, Ezio; L., Mariani, Leonardo; D., Ničković, Dejan; D., Yadav, Drishti",
        Title="Property-Based Mutation Testing",
        Year=2023,
        Source_title="IEEE International Conference on Software Testing, Verification and Validation (ICST)",
        Document_Type="Conference paper", Cited_by=10,
        DOI="10.1109/ICST57152.2023.00029", RQ="RQ1: Mutation operators",
    ),
    # ---------------------------- RQ2 --------------------------------------
    dict(
        Authors="A., Arcuri, Andrea; A., Poth, Alexander; O., Rrjolli, Olsi",
        Title="Fuzzing REST APIs in Industry: Necessary Features and Open Problems",
        Year=2026, Source_title="arXiv", Document_Type="Preprint", Cited_by=0,
        DOI="10.48550/arXiv.2604.01759", RQ="RQ2: Limitations & challenges",
    ),
    dict(
        Authors="M., Zhang, Man; C., Shen, Chongyang; A., Arcuri, Andrea",
        Title="Detecting and Mitigating Flakiness in REST API Fuzzing",
        Year=2026, Source_title="arXiv", Document_Type="Preprint", Cited_by=0,
        DOI="10.48550/arXiv.2603.28452", RQ="RQ2: Limitations & challenges",
    ),
    # ---------------------------- RQ3 --------------------------------------
    dict(
        Authors="S., Seran, Susruthan; G., Bhandari, Guru; A., Arcuri, Andrea",
        Title="Detecting Server-Side Request Forgery (SSRF) Vulnerabilities in REST API Fuzz Testing",
        Year=2026, Source_title="ACM International Workshop Proceedings",
        Document_Type="Conference paper", Cited_by=0,
        DOI="10.1145/3786155.3788581", RQ="RQ3: Vulnerability factors",
    ),
    dict(
        Authors="T., Rooijakkers, Thomas; A., Nijsten, Anne; C., Daniele, Cristian; E., Weitenberg, Erieke; R., Groenewegen, Ringo; A., Melissen, Arthur",
        Title="WuppieFuzz: Coverage-Guided, Stateful REST API Fuzzing",
        Year=2026,
        Source_title="International Conference on Evaluation of Novel Approaches to Software Engineering, ENASE - Proceedings",
        Document_Type="Conference paper", Cited_by=0,
        DOI="10.5220/0014327000004061", RQ="RQ3: Vulnerability factors",
    ),
    dict(
        Authors="V., Gadey, Varun; C., Sendner, Christoph; K., Zimmermann, Keven; A., Dmitrienko, Alexandra",
        Title="RESTing-LLAMA: Large Language Model Based REST API Fuzzing",
        Year=2026, Source_title="ACM Conference Proceedings",
        Document_Type="Conference paper", Cited_by=0,
        DOI="10.1145/3779208.3785383", RQ="RQ3: Vulnerability factors",
    ),
    dict(
        Authors="Z., He, Zhuofeng; S., Shang, Sunpei; Y., Guo, Yumeng; A., Zhou, Aojie",
        Title="Spec2SeqFuzz: A Category Prediction-Guided Approach for Stateful Multi-Step REST API Fuzzing",
        Year=2026, Source_title="Electronics", Document_Type="Article", Cited_by=0,
        DOI="10.3390/electronics15112309", RQ="RQ3: Vulnerability factors",
    ),
    dict(
        Authors="D., Yang, Ding; R., Qian, Ruixiang; Z., Wei, Zhao; C., Fang, Chunrong",
        Title="Log-Based, Business-Aware REST API Testing",
        Year=2026, Source_title="arXiv", Document_Type="Preprint", Cited_by=0,
        DOI="10.48550/arXiv.2604.08007", RQ="RQ3: Vulnerability factors",
    ),
    # ---------------------------- RQ4 --------------------------------------
    dict(
        Authors="A., Almjnoony, Ayman; R., Alshamrani, Rayan; J., Alves-Foss, Jim; F., Sheldon, Frederick T.",
        Title="Bridging the Gap in Web API Security: A Systematic Review of Vulnerabilities, Misuse Patterns, and Developer Challenges",
        Year=2026, Source_title="Software", Document_Type="Review", Cited_by=0,
        DOI="10.3390/software5020025", RQ="RQ4: Mitigation strategies",
    ),
    # ---------------------------- RQ5 --------------------------------------
    dict(
        Authors="Y., Levi, Yarin; R., Dubin, Ran",
        Title="API Security Based on Automatic OpenAPI Mapping",
        Year=2026, Source_title="arXiv", Document_Type="Preprint", Cited_by=0,
        DOI="10.48550/arXiv.2604.19471", RQ="RQ5: Security misconfigurations",
    ),
    dict(
        Authors="M., Hakim, Muhammad Ikhwanul",
        Title="Performance Analysis of the Fuzzing Method in Detecting API Vulnerabilities in Mobile Healthcare Application X Based on OWASP API Security Top 10",
        Year=2026, Source_title="Telematika", Document_Type="Article", Cited_by=0,
        DOI="10.35671/telematika.v19i1.3149", RQ="RQ5: Security misconfigurations",
    ),
]

RQ_ORDER = [
    "RQ1: Mutation operators",
    "RQ2: Limitations & challenges",
    "RQ3: Vulnerability factors",
    "RQ4: Mitigation strategies",
    "RQ5: Security misconfigurations",
]


def backup(path: Path) -> None:
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak.20260802"))


def build_rows() -> pd.DataFrame:
    rows = []
    for r in UPDATE_RECORDS:
        rows.append({
            "Authors": r["Authors"],
            "Author full names": r["Authors"],
            "Title": r["Title"],
            "Year": r["Year"],
            "Source title": r["Source_title"],
            "Document Type": r["Document_Type"],
            "Cited by": r["Cited_by"],
            "DOI": r["DOI"],
            "Author Keywords": "",
            "Index Keywords": "",
            "Affiliations": "",
            "Language of Original Document": "English",
            "Open Access": "",
            "Source": STREAM,
            "EID": "",
            "RQ": r["RQ"],
        })
    return pd.DataFrame(rows)


def main() -> int:
    corpus_path = BIBLIO / "corpus_unificado.csv"
    corpus = pd.read_csv(corpus_path)

    # Idempotence: drop any previously appended update stream before re-adding.
    if "Source" in corpus.columns:
        corpus = corpus[corpus["Source"] != STREAM].copy()

    # ---------------- language eligibility ----------------
    # The protocol restricts the review to publications in English. Six records
    # retained by earlier passes are not in English (five Chinese, one Spanish),
    # covering five distinct studies since one is assigned to two research
    # questions. They are removed here so that the corpus matches the stated
    # criterion, and the count is reported as a full-text exclusion reason in
    # the PRISMA flow diagram.
    # ---------------- container records ----------------
    # One Scopus record is the proceedings volume of a conference, not a study:
    # Document Type "Conference review", no author, no DOI. It was swept up by
    # the query and cannot be a primary study, so it is removed here.
    container = corpus["Document Type"].fillna("").str.strip().str.lower() == "conference review"
    if container.any():
        print(f"container exclusion: dropping {int(container.sum())} proceedings-volume record(s)")
        corpus = corpus[~container].copy()

    lang = corpus["Language of Original Document"].fillna("English")
    non_english = corpus[~lang.str.contains("English", na=False)]
    if len(non_english):
        print(f"language exclusion: dropping {len(non_english)} rows "
              f"({non_english['Title'].nunique()} distinct studies) not in English")
        corpus = corpus[lang.str.contains("English", na=False)].copy()

    base_n = len(corpus)
    new = build_rows()

    merged = pd.concat([corpus, new], ignore_index=True)
    merged["Article_ID"] = range(1, len(merged) + 1)
    cols = ["Article_ID"] + [c for c in merged.columns if c != "Article_ID"]
    merged = merged[cols]

    # ---------------- re-screening exclusions ----------------
    # The term "mutation" is a homonym: it names a genetic operator in
    # evolutionary computation and a point substitution in molecular biology.
    # Run without a software-testing anchor the search retrieved cloud task
    # scheduling, QoS service composition and RNA structure comparison, none of
    # which satisfies the review's own exclusion criteria. The 2026-08-03
    # re-screening judged every record against those criteria and gave each
    # proposed exclusion to an independent adjudicator; the survivors are listed
    # in rescreening_exclusions.json with the evidence that decided them.
    #
    # Keyed on normalized title rather than Article_ID, which is reassigned on
    # every run of this script and would silently drift.
    excl_path = BASE / "rescreening_exclusions.json"
    if excl_path.exists():
        import json as _json
        import re as _re

        def _key(s):
            return _re.sub(r"[^a-z0-9]", "", str(s or "").lower())

        excluded = {e["title_key"] for e in _json.loads(excl_path.read_text(encoding="utf-8"))}
        mask = merged["Title"].map(_key).isin(excluded)
        if mask.any():
            print(f"re-screening exclusion: dropping {int(mask.sum())} rows "
                  f"({merged.loc[mask, 'Title'].nunique()} distinct studies) "
                  f"outside the review scope")
            merged = merged[~mask].copy()
            merged["Article_ID"] = range(1, len(merged) + 1)

    backup(corpus_path)
    merged.to_csv(corpus_path, index=False)
    print(f"corpus_unificado.csv: {base_n} -> {len(merged)} RQ-assignments "
          f"(+{len(new)} from the {STREAM} stream)")

    # ---------------- articles per RQ ----------------
    per_rq = merged["RQ"].value_counts().reindex(RQ_ORDER)
    out = pd.DataFrame({"RQ": RQ_ORDER, "N_articulos": per_rq.values})
    backup(BIBLIO / "articulos_por_RQ.csv")
    out.to_csv(BIBLIO / "articulos_por_RQ.csv", index=False)
    print("articulos_por_RQ.csv:", dict(zip(out["RQ"], out["N_articulos"])))

    # ---------------- citations per RQ ----------------
    merged["Cited by"] = pd.to_numeric(merged["Cited by"], errors="coerce").fillna(0)
    grp = merged.groupby("RQ")["Cited by"]
    cit = pd.DataFrame({
        "RQ": RQ_ORDER,
        "count": [int(grp.count().get(rq, 0)) for rq in RQ_ORDER],
        "mean": [float(grp.mean().get(rq, 0)) for rq in RQ_ORDER],
        "median": [float(grp.median().get(rq, 0)) for rq in RQ_ORDER],
        "max": [int(grp.max().get(rq, 0)) for rq in RQ_ORDER],
    })
    backup(BIBLIO / "citas_por_RQ.csv")
    cit.to_csv(BIBLIO / "citas_por_RQ.csv", index=False)
    print("citas_por_RQ.csv:")
    for _, r in cit.iterrows():
        print(f"   {r['RQ']}: n={int(r['count'])} mean={r['mean']:.1f} "
              f"median={r['median']:.1f} max={int(r['max'])}")

    # ---------------- publications per year ----------------
    yr = merged.dropna(subset=["Year"]).copy()
    yr["Year"] = yr["Year"].astype(int)
    per_year = yr.groupby("Year").size().reset_index(name="N_articulos")
    backup(BIBLIO / "pubs_por_anio.csv")
    per_year.to_csv(BIBLIO / "pubs_por_anio.csv", index=False)
    print("pubs_por_anio.csv:", per_year.tail(4).to_dict("records"))

    # ---------------- document types ----------------
    dt = merged["Document Type"].fillna("Unknown").value_counts()
    dt_df = dt.reset_index()
    dt_df.columns = ["Document Type", "N_articulos"]
    backup(BIBLIO / "pubs_por_tipo_documento.csv")
    dt_df.to_csv(BIBLIO / "pubs_por_tipo_documento.csv", index=False)
    print("pubs_por_tipo_documento.csv:", dict(zip(dt_df["Document Type"], dt_df["N_articulos"])))

    # ---------------- venues ----------------
    # Records without a venue field are dropped, as in the original pipeline.
    src = merged["Source title"].dropna().value_counts()
    src_df = src.reset_index()
    src_df.columns = ["Source title", "N_articulos"]
    backup(BIBLIO / "pubs_por_fuente.csv")
    src_df.to_csv(BIBLIO / "pubs_por_fuente.csv", index=False)
    print("pubs_por_fuente.csv top5:", src_df.head(5).to_dict("records"))

    # ---------------- per-RQ source split ----------------
    # Derived from corpus_unificado so that this table and articulos_por_RQ.csv
    # report the same population. The previous version was computed from a
    # separate consolidated export that never agreed with the corpus (149 vs
    # 154 rows before this update), which put two mutually inconsistent per-RQ
    # totals on facing pages of the chapter.
    #
    # The corpus records three provenance streams. Their labels are historical;
    # the mapping to the streams the methodology describes is:
    #   Scopus                -> the database-query stream
    #   slr-update            -> citation chasing and forward-snowballing
    #   Search update 2026-08 -> the citation index
    # The corpus does not carry a per-record Scopus/Web of Science split, so the
    # figure reports the database stream as one series. The identified-record
    # split (159 and 40) is reported in the prose, where it is documented.
    STREAM_LABEL = {
        "Scopus": "Database queries",
        "slr-update": "Citation chasing",
        STREAM: "Citation index",
    }
    merged["Stream"] = merged["Source"].map(
        lambda s: STREAM_LABEL.get(s, "Database queries"))
    ct = pd.crosstab(merged["RQ"], merged["Stream"]).reindex(RQ_ORDER).fillna(0)
    cols = ["Database queries", "Citation chasing", "Citation index"]
    for c in cols:
        if c not in ct.columns:
            ct[c] = 0
    stats = pd.DataFrame({"Research Question": RQ_ORDER})
    for c in cols:
        stats[c] = [int(ct.loc[rq, c]) for rq in RQ_ORDER]
    stats["Total Articles"] = stats[cols].sum(axis=1)
    total = {"Research Question": "TOTAL"}
    for c in cols + ["Total Articles"]:
        total[c] = int(stats[c].sum())
    stats = pd.concat([stats, pd.DataFrame([total])], ignore_index=True)
    stats_path = CONSOLIDATED / "systematic_review_summary_stats.csv"
    backup(stats_path)
    stats.to_csv(stats_path, index=False)
    print("summary_stats.csv:", total)

    studies = merged["Title"].nunique()
    print(f"\nPrimary studies: {studies}   RQ-assignments: {len(merged)}   "
          f"ratio {len(merged)/studies:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
