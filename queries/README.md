# Search queries

One file per research question per database.

| Question | Subject |
|---|---|
| RQ1 | Mutation operators developed for testing the security of RESTful APIs |
| RQ2 | Limitations and challenges of current mutation operators |
| RQ3 | Factors that contribute to finding vulnerabilities in RESTful APIs |
| RQ4 | Strategies used to mitigate vulnerabilities in RESTful APIs |
| RQ5 | Common security misconfigurations in RESTful API development |

```
rq<n>-scopus.txt   the string for Scopus
rq<n>-wos.txt      the string for Web of Science
queries.json       all ten, machine-readable
```

## Running them by hand

Paste the block into the `TITLE-ABS-KEY` field in Scopus or the `TS` field in
Web of Science. Line breaks in the files are for reading; the interface treats
the string as one line.

Set these filters in the interface, since they are not part of the strings:

- publication years 2000 to 2026
- document types article, conference paper, review, book chapter
- language English

## Running them through the APIs

`../scripts/probe_totals.py` reports how many records each query returns and how
many requests paginating it would cost. Run it first: the Web of Science Starter
API allows fifty requests per day and one per second, and a blind run can spend
the day's allowance on one question.

`../scripts/run_search.py` executes every query against both databases and
writes the retrieved records as JSON.

```bash
export SCOPUS_API_KEY=...      # https://dev.elsevier.com/
export WOS_API_KEY=...         # https://developer.clarivate.com/

python3 ../scripts/probe_totals.py
python3 ../scripts/run_search.py
```

## Regenerating these files

The executable definitions are in `../scripts/queries.py`, and
`../scripts/export_queries.py` rebuilds this directory from them, so the text
files cannot drift from the strings that execute.
