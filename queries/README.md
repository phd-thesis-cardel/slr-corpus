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
| RQ3 | 3778 | 26/28 | 12/12 | too broad |
| RQ4 | 478 | 2/2 | 1/1 | too broad |
| RQ5 | 149 | 1/9 | 0/18 | recall lost |

The figures are computed from the result sets deposited in this repository and
can be recomputed. Narrower variants were tried for the last three questions. A
tighter RQ3 came down to 214 records but recall fell to 18/28, and a tighter RQ4
came down to 99 while holding recall; neither result set was retained, so neither
appears above. No variant of RQ5 reached an acceptable trade-off: every candidate
either returned thousands of records or recovered one of the nine studies the
database search had found.

The reason is structural rather than a matter of term choice. A corpus assembled
with a loose net and then reduced by screening is not recoverable by a tight net.
Reproducing it takes the screening decisions, which is why they are published in
`../data/screening_decisions.json` rather than left implicit in a query string.

## Files

`published/` and `corrected/` hold one plain-text file per question per
database, ready to paste into the Scopus or Web of Science interface. Each
carries the question it answers and, in the corrected set, the change that was
made and why.

`queries.json` carries both forms as one machine-readable document.

The executable definitions the pipeline runs are `../scripts/queries.py` and
`../scripts/queries_v2.py`; `../scripts/export_queries.py` regenerates
everything in this directory from them, so the text files cannot drift from the
strings that actually execute.
