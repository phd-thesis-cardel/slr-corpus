---
title: Audit of the search strings
author: Carlos A. Delgado S.
date: 2026-08-03
version: 1.0
status: final
tags: [slr, search, reproducibility, audit]
---

# Audit of the search strings

The published queries were re-executed against the Scopus API in August 2026 and
compared with the exported records the review had kept. They do not match, and
the mismatch is not a matter of syntax. This document reports what was measured,
what changed in the corrected strings, and where the correction did not work.

## The published query did not constrain the result

For the first research question the export holds eighteen records while the
published string returns one. Measured against the whole Scopus index, the
mutation block and the published interface block intersect in seven records, so
a search that returned eighteen cannot have applied that block as written.

The eighteen records satisfy the mutation block and the security block but not
the interface block. That places the search that ran closer to
`mutation AND security` than to the three-block string that was written down.
The interface block was published, but it passed the result through.

The uniform filters tell the same story. Years, document types and language were
applied through the database interface at search time and were never part of the
recorded string, which is why the first re-execution retrieved proceedings
volumes the original search had never seen.

## The term *mutation* is a homonym

`mutation operator` names a variation operator in evolutionary computation, and
`mutation` names a point substitution in molecular biology. Both senses were
retrieved. Of the eighteen records the first question returned, four are
evolutionary-computation papers on cloud task scheduling and image encryption,
and one study elsewhere in the corpus compares RNA secondary structures.

Forty-six records that reached the corpus fall outside the review's own
exclusion criteria on this basis, or on the equally generic third block of the
misconfiguration query. Each is listed in `rescreening-evidence.md` with the
abstract fragment that decided it.

## What the corrected strings change

**A software-testing anchor.** The corrected form for RQ1 and RQ2 requires a
testing term to co-occur with the mutation block, which removes the evolutionary
and biological senses.

**A wider interface block.** The published block reads
`"REST* API*" OR "Cloud* API*" OR "Web API*"`. As a quoted phrase carrying
wildcards it behaves loosely. The corrected block names the service vocabulary
the corpus contains, which is what the review means by its broad bibliometric
scope, and it binds instead of passing the result through.

**A security block for RQ5.** The published query paired `configuration*` with
`development*`, terms general enough that any paper mentioning a REST API and
its deployment matched. That query admitted the largest share of off-topic
records.

## What the correction achieved

Recall counts only studies whose provenance is the database search: studies
reached by citation chasing or by the citation-index pass are not retrievable by
a database query and would depress the score unfairly. Leakage counts studies
the re-screening excluded that the corrected query brings back.

| RQ | Retrieved | Recall | Leakage | Verdict |
|---|---|---|---|---|
| RQ1 | 18 | 13/13 | 1/4 | corrected |
| RQ2 | 27 | 11/13 | 0/11 | corrected |
| RQ3 | 3778 | 26/28 | 12/12 | too broad |
| RQ4 | 478 | 2/2 | 1/1 | too broad |
| RQ5 | 149 | 1/9 | 0/18 | recall lost |

The figures are computed from the result sets deposited in this repository and
can be recomputed with `../scripts/rerun_search.py`.

Narrower variants were tried for the last three questions. A tighter RQ3 came
down to 214 records but recall fell to 18/28, and a tighter RQ4 came down to 99
while holding recall; neither result set was retained, so neither appears in the
table. No variant of RQ5 reached an acceptable trade-off: every candidate either
returned thousands of records or recovered one of the nine studies the database
search had found. `../scripts/tune_queries.py` runs the candidates and scores
them.

## Why the last three questions did not resolve

The reason is structural rather than a matter of term choice. A corpus assembled
with a loose net and then reduced by screening is not recoverable by a tight
net: the studies that survived screening are heterogeneous precisely because the
net that caught them was wide.

Reproducing the corpus therefore takes the screening decisions, not a better
query. That is why they are published in `../data/screening_decisions.json`,
with the reason and a verbatim source fragment behind every exclusion, rather
than left implicit in a query string.
