# Search queries

The five research questions of the review, each with the string that was run
against Scopus and against Web of Science.

| Question | Subject |
|---|---|
| RQ1 | Mutation operators developed for testing the security of RESTful APIs |
| RQ2 | Limitations and challenges of current mutation operators |
| RQ3 | Factors that contribute to finding vulnerabilities in RESTful APIs |
| RQ4 | Strategies used to mitigate vulnerabilities in RESTful APIs |
| RQ5 | Common security misconfigurations in RESTful API development |

## Layout

```
published/     the strings as they appear in the review        (10 files)
corrected/     the strings an update should use instead        (10 files)
queries.json   both forms, machine-readable
```

One file per question per database, named `rq<n>-scopus.txt` and
`rq<n>-wos.txt`. Each carries the question it answers as a comment header and,
in `corrected/`, the change that was made. The query itself follows, wrapped for
reading; the database interface treats it as a single line.

## Running them

Paste the block into the `TITLE-ABS-KEY` field in Scopus or the `TS` field in
Web of Science. The Scopus strings in `corrected/` carry their year, document
type and language filters inline, so nothing has to be set in the interface. The
published strings do not: those filters were applied through the interface at
search time and were never part of the recorded string.

Both forms are constrained to publication years 2000 to 2026, to the document
types article, conference paper, review and book chapter, and to English.

To run them through the APIs instead, `../scripts/rerun_search.py` executes
every query and scores the result against the screened corpus, and
`../scripts/probe_totals.py` reports what each one costs to paginate before any
quota is spent.

## Why there are two forms

The published form is what the review reports. The corrected form removes two
defects that a 2026 audit established: the term *mutation* is a homonym shared
with evolutionary computation and molecular biology, and the interface block of
the published string did not constrain the result.

The corrected form is not a reconstruction of what was executed. The string that
ran was not recorded at the time, and the audit could only establish what it was
*not*. Use `corrected/` for an update; cite `published/` as the review's method.

`../docs/query-audit.md` reports the audit: what each change was, and how recall
and precision moved when the corrected strings were measured against the
screened corpus.

## Regenerating

The executable definitions are `../scripts/queries.py` and
`../scripts/queries_v2.py`. `../scripts/export_queries.py` rebuilds everything
in this directory from them, so the text files cannot drift from the strings
that actually execute.
