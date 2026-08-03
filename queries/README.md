# Search queries

Two forms of every query are recorded. The `published` form is the string that
appears in the review. The `corrected` form is the string an update should use,
with the defects the August 2026 audit established removed.

They are kept apart on purpose. The corrected form is not a reconstruction of
what was executed; the string that was executed was not recorded at the time, and
the audit could only establish what it was *not*.

## Uniform filters

Both forms are constrained to publication years 2000 to 2026, to the document
types article, conference paper, review and book chapter, and to English. In the
published form these filters were applied through the database interface and were
not part of the recorded string, which is why the first re-execution retrieved
proceedings volumes that the original search had never seen.

## What changed, and why

**A software-testing anchor.** `mutation operator` is a term of art in
evolutionary computation, and `mutation` is one in molecular biology. Both senses
were retrieved. The corrected form for RQ1 and RQ2 requires a testing term to
co-occur, which removes them.

**A wider interface block.** The published block reads
`"REST* API*" OR "Cloud* API*" OR "Web API*"`. As a quoted phrase carrying
wildcards this behaves loosely, and measured against the whole Scopus index it
intersects the mutation block in seven records. The corrected block names the
service vocabulary the corpus actually contains, which is what the review means
by its broad bibliometric scope, and constrains the result instead of passing it
through.

**A mandatory security block for RQ5.** The published query paired
`configuration*` with `development*`, terms general enough that any paper
mentioning a REST API and its deployment matched. This query admitted the largest
share of off-topic records.

## Measured effect

Recall counts only studies whose provenance is the database search; studies
reached by citation chasing or by the citation-index pass are not retrievable by
a database query. Leakage counts studies the re-screening excluded that the
corrected query brings back.

| RQ | Retrieved | Recall | Leakage | Verdict |
|---|---|---|---|---|
| RQ1 | 18 | 13/13 | 1/4 | corrected |
| RQ2 | 27 | 11/13 | 0/11 | corrected |
| RQ3 | 214 | 18/28 | 8/12 | not resolved |
| RQ4 | 99 | 2/2 | 1/3 | improved |
| RQ5 | — | — | — | not resolved |

For RQ3 and RQ5 no candidate reached an acceptable trade-off. Every variant
either returned thousands of records or lost half the retained corpus. The reason
is structural rather than a matter of term choice: a corpus assembled with a
loose net and reduced by screening is not recoverable by a tight net. Reproducing
it requires the screening decisions, which is why they are published in
`../data/screening_decisions.json` rather than left implicit in a query string.

Machine-readable strings are in `queries.py` (published) and `queries_v2.py`
(corrected), both under `../scripts/`.
