# Systematic review corpus: mutation testing for RESTful API security

Reproducibility artifact for a systematic literature review on mutation testing
applied to the security evaluation of RESTful APIs, covering the publication
window 2000–2026.

This repository holds the search queries, the per-study screening decisions with
the evidence behind each one, the derived aggregate tables, and the code that
produces them from the corpus. It is the deposit referenced by the review as the
fulfilment of PRISMA 2020 item 17.

## What is here

| Path | Contents |
|---|---|
| `queries/` | Search strings per research question, per database, in both the originally executed and the corrected form |
| `data/screening_decisions.json` | Every retrieved study with its inclusion or exclusion decision, the reason, and a verbatim fragment of the source supporting that reason |
| `data/corpus.csv` | The included studies with author, year, title, venue, DOI, provenance and research-question assignment |
| `docs/` | The re-screening evidence document and the methodological notes |
| `scripts/` | The pipeline: query probes, search execution, screening-set construction, evidence export |
| `figures/` | Bibliometric figures and the code that derives them |

## Corpus at a glance

| | |
|---|---|
| Records identified | 300 |
| Retrieved and screened | 160 |
| Included after screening | **114** |
| Excluded at re-screening | 46 |
| Research-question assignments | 116 |

Per question: RQ1 21, RQ2 18, RQ3 50, RQ4 12, RQ5 15. Two studies address two
questions each, which is why the assignments exceed the study count. By
provenance: 65 assignments from the database queries, 36 from citation chasing,
15 from the citation index.

Every included study carries a publication venue and 103 of the 114 carry a
Digital Object Identifier. Venues absent from the unified corpus were recovered
from the raw exports and, failing that, from the DOI registry; one truncated
identifier was repaired against a title search.

## Research questions

1. What mutation operators have been developed and used for testing the security of RESTful APIs?
2. What limitations or challenges are associated with current mutation operators?
3. What factors contribute to finding vulnerabilities in RESTful APIs?
4. What strategies are used to mitigate vulnerabilities in RESTful APIs?
5. What are the most common security misconfigurations encountered during the development of RESTful APIs?

## Two things a reader should know before reusing this corpus

### The published query is stricter than the search that produced the corpus

An audit run in August 2026 executed the published query strings against the
Scopus API and compared the result with the exported records. They do not match.
For the first research question the export holds eighteen records while the
published string returns one, and the discrepancy is not a matter of syntax:
measured against the whole Scopus index, the mutation block and the interface
block intersect in seven records. A search returning eighteen cannot have applied
the interface block as published.

The records in the export satisfy the mutation block and the security block but
not the interface block, which places the search that was actually run closer to
`mutation AND security` than to the three-block string that was written down. The
interface block was published but did not constrain the result.

Both forms are recorded in `queries/`. The corrected strings are offered as the
basis for future updates, not as a reconstruction of what ran.

### The search term "mutation" is a homonym and the corpus paid for it

`mutation operator` names a genetic operator in evolutionary computation, and
`mutation` names a point substitution in molecular biology. Neither sense is the
subject of this review. Without a software-testing anchor the search retrieved
cloud task-scheduling papers, QoS service-composition papers solved by genetic
algorithms, and one paper on RNA secondary-structure comparison.

Forty-six of the one hundred and sixty screened records fall outside the
review's own exclusion criteria on this basis or on the equally generic third
block of the misconfiguration query. Two further records were withdrawn in a
first pass and reinstated: both were judged on title alone, no abstract being
available, and the review itself cites them as evidence on dynamic authorization
and transport encryption for REST API calls. A decision that the argument of the
review contradicts is a decision to revisit. Every one of them is listed in
`docs/rescreening-evidence.md` with the abstract fragment that decided it, and
each proposed exclusion was given to an independent adjudicator instructed to
rescue it if any honest reading placed it inside scope. Nine were rescued and
remain in the corpus.

A corrected query for the first two questions removes the homonym cleanly: with a
software-testing anchor, recall over the database-sourced studies holds at 13/13
and 11/13 while leakage of excluded studies falls to 1/4 and 0/11. For the third
and fifth questions no candidate reached an acceptable trade-off, because a
corpus assembled with a loose net is not recoverable with a tight one. That
limitation is stated rather than hidden.

## Redistribution

The records here are limited to bibliographic facts: authors, title, year,
venue, DOI, document type, provenance, and the review's own screening decisions.
Abstracts, indexed keyword fields, affiliation data and citation counts from
Scopus and Web of Science are not redistributed, since those are the indexing
value-add of their vendors; `scripts/` retrieves them again from the APIs under
the reader's own credentials.

The exclusion evidence quotes a fragment of each excluded study's abstract,
averaging under two hundred characters, because a screening decision that cannot
be checked against its source is not a decision a reader can audit. Aggregate
tables in `data/` are derived from the withheld fields but do not reproduce
them.

## Reproducing

```bash
export SCOPUS_API_KEY=...      # https://dev.elsevier.com/
export WOS_API_KEY=...         # https://developer.clarivate.com/

python3 scripts/probe_totals.py       # size the searches before running them
python3 scripts/rerun_search.py       # execute and score against the screened corpus
```

The Web of Science Starter API permits fifty requests per day and one per
second. `probe_totals.py` reports the pagination cost of each question so a run
can be budgeted rather than abandoned half way.

## Licence

Data under [CC BY 4.0](LICENSE-DATA). Code under [MIT](LICENSE-CODE).
