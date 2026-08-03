# Systematic review corpus: mutation testing for RESTful API security

Reproducibility artifact for a systematic literature review on mutation testing
applied to the security evaluation of RESTful APIs, over the publication window
2000 to 2026.

It holds the corpus, the screening decision behind every study, the search
queries, the aggregate tables, and the code that derives them.

## Corpus

| | |
|---|---|
| Records identified | 300 |
| Retrieved and screened | 160 |
| Included | **114** |
| Research-question assignments | 116 |

Per question: RQ1 21, RQ2 18, RQ3 50, RQ4 12, RQ5 15. Two studies answer two
questions each, which is why the assignments exceed the study count. By
provenance: 65 assignments from the database queries, 36 from citation chasing,
15 from a citation index.

Every included study carries a publication venue, and 103 of the 114 carry a
Digital Object Identifier.

## Research questions

1. What mutation operators have been developed and used for testing the security of RESTful APIs?
2. What limitations or challenges are associated with current mutation operators?
3. What factors contribute to finding vulnerabilities in RESTful APIs?
4. What strategies are used to mitigate vulnerabilities in RESTful APIs?
5. What are the most common security misconfigurations encountered during the development of RESTful APIs?

## What is here

| Path | Contents |
|---|---|
| `data/corpus.csv` | The 114 included studies: authors, year, title, venue, DOI, question, provenance |
| `data/primary-studies.bib` | The same studies as BibTeX, keyed `S1` to `S114` |
| `data/screening_decisions.json` | All 160 retrieved studies with the decision on each, the reason, and a verbatim fragment of the source behind every exclusion |
| `data/*.csv` | The aggregates behind each figure: per year, per venue, per document type, per question, per keyword, per author |
| `queries/` | The search string for each question and each database |
| `figures/` | The bibliometric figures |
| `scripts/` | The pipeline that produces all of the above |
|  `docs/screening-evidence.md` | The excluded studies grouped by question, each with its evidence |

## Reproducing

The aggregates and the figures derive from `data/corpus.csv`, so they rebuild
without touching a database:

```bash
pip install pandas matplotlib networkx

python3 scripts/rebuild_author_aggregates.py    # author and co-authorship tables
python3 scripts/export_screening_evidence.py   # evidence document
```

To run the searches themselves, see `queries/README.md`. Both APIs need a key of
your own, and the Web of Science Starter API allows fifty requests per day.

## What this artifact does not redistribute

The corpus carries bibliographic facts: authors, title, year, venue, identifier,
document type, provenance, and this review's own screening decisions.

Abstracts, indexed keyword fields, affiliations and citation counts are the
indexing work of Scopus and Web of Science and are not redistributed here. The
scripts retrieve them again from both interfaces under your own credentials.
Aggregates derived from those fields are included; the fields themselves are
not.

The exclusion evidence quotes a fragment of each excluded study's abstract,
under two hundred characters, so that a screening decision can be checked
against the source it rests on.

## Licence

Data under [CC BY 4.0](LICENSE-DATA). Code under [MIT](LICENSE-CODE).
