"""Corrected search queries for the five research questions.

The queries originally published with the review suffer from two defects that
the 2026-08-03 audit established empirically.

First, homonymy. The term "mutation operator" names a genetic operator in
evolutionary computation and a point mutation in molecular biology, and neither
sense is the subject of this review. Run without a software-testing anchor, the
mutation block retrieved cloud task-scheduling, QoS service-composition and
RNA-structure papers, forty-eight of which reached the corpus.

Second, an interface block that never constrained the result. Measured against
Scopus, the mutation block intersects the published API block in seven records
across the whole index, so a search returning eighteen records for RQ1 cannot
have applied that block as written. The corrected block widens the interface
vocabulary to the web-service and microservice terms the corpus actually
contains, which is both what the review means by its bibliometric scope and
what makes the block bind.

Uniform database-side filters (publication years, document types, English) are
declared once here rather than left implicit, since their absence is what let
proceedings volumes into the result set.

Each entry carries the original string under "legacy" so that the change is
auditable rather than silent.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Shared term blocks
# ---------------------------------------------------------------------------

# Mutation, restricted to the software-testing sense by the anchor below.
MUT_SCOPUS = (
    '"mutation testing" OR "mutation analysis" OR "mutation operator*" '
    'OR "mutant*" OR "mutation score" OR "mutation adequacy"'
)
MUT_WOS = (
    '"mutation testing" OR "mutation analysis" OR "mutation operator*" '
    'OR "mutant*" OR "mutation score" OR "mutation adequacy"'
)

# Software-testing anchor. Disambiguates the mutation block away from
# evolutionary computation and molecular biology.
TEST_SCOPUS = (
    '"software testing" OR "test case*" OR "test suite*" OR "test generation" '
    'OR "testing technique*" OR "test adequacy" OR "fault detection" '
    'OR "test data" OR "unit test*"'
)
TEST_WOS = TEST_SCOPUS

# Interface block: REST and the adjacent service vocabulary the review admits.
API_SCOPUS = (
    '"REST API" OR "RESTful API" OR "web API" OR "cloud API" OR "HTTP API" '
    'OR "web service*" OR "microservice*" OR "API security" OR "API testing" '
    'OR "OpenAPI" OR "service composition"'
)
API_WOS = API_SCOPUS

# Security block.
SEC_SCOPUS = "security* OR vulnerabilit* OR privac* OR misconfigur*"
SEC_WOS = SEC_SCOPUS

# Uniform database-side filters.
YEAR_FROM, YEAR_TO = 2000, 2026
SCOPUS_FILTERS = (
    f"PUBYEAR > {YEAR_FROM - 1} AND PUBYEAR < {YEAR_TO + 1} "
    "AND (DOCTYPE(ar) OR DOCTYPE(cp) OR DOCTYPE(re) OR DOCTYPE(ch)) "
    "AND LANGUAGE(english)"
)
WOS_FILTERS = f"PY=({YEAR_FROM}-{YEAR_TO})"


def _scopus(*blocks: str) -> str:
    body = " AND ".join(f"TITLE-ABS-KEY({b})" for b in blocks)
    return f"{body} AND {SCOPUS_FILTERS}"


def _wos(*blocks: str) -> str:
    body = " AND ".join(f"TS=({b})" for b in blocks)
    return f"{body} AND {WOS_FILTERS}"


QUERIES_V2 = [
    {
        "rq": "RQ1",
        "description": (
            "What mutation operators have been developed and used for testing "
            "the security of RESTful APIs?"
        ),
        "change": (
            "Interface block widened to web services and microservices; "
            "document-type and language filters made explicit."
        ),
        "scopus": _scopus(MUT_SCOPUS, API_SCOPUS, SEC_SCOPUS),
        "wos": _wos(MUT_WOS, API_WOS, SEC_WOS),
        "legacy_scopus": (
            'TITLE-ABS-KEY("mutation testing" OR "mutation operator*" OR "software mutation*" '
            'OR "program mutation*" OR "mutation analysis") '
            'AND TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TITLE-ABS-KEY("security*" OR "vulnerabilit*" OR "privac*")'
        ),
    },
    {
        "rq": "RQ2",
        "description": (
            "What limitations or challenges are associated with current "
            "mutation operators?"
        ),
        "change": (
            "Software-testing anchor added. The original third block "
            "(limitation, challenge, drawback, issue) is too generic to "
            "disambiguate the mutation homonym on its own."
        ),
        "scopus": _scopus(
            MUT_SCOPUS,
            TEST_SCOPUS,
            API_SCOPUS,
            "limitation* OR challenge* OR drawback* OR issue* OR problem*",
        ),
        "wos": _wos(
            MUT_WOS,
            TEST_WOS,
            API_WOS,
            "limitation* OR challenge* OR drawback* OR issue* OR problem*",
        ),
        "legacy_scopus": (
            'TITLE-ABS-KEY("mutation testing" OR "mutation operator*" OR "software mutation*" '
            'OR "program mutation*" OR "mutation analysis") '
            'AND TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            "AND TITLE-ABS-KEY(limitation* OR challenge* OR drawback* OR issue*)"
        ),
    },
    {
        "rq": "RQ3",
        "description": (
            "What factors contribute to finding vulnerabilities in RESTful APIs?"
        ),
        "change": (
            "Interface block widened; security terms tightened so that the "
            "generic cause/factor/source block no longer carries the query."
        ),
        "scopus": _scopus(
            API_SCOPUS,
            'vulnerabilit* OR "security flaw*" OR exploit* OR "attack*" OR "security defect*"',
            'cause* OR factor* OR source* OR "root cause*" OR detect* OR discover*',
        ),
        "wos": _wos(
            API_WOS,
            'vulnerabilit* OR "security flaw*" OR exploit* OR attack* OR "security defect*"',
            'cause* OR factor* OR source* OR "root cause*" OR detect* OR discover*',
        ),
        "legacy_scopus": (
            'TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TITLE-ABS-KEY("vulnerability" OR "security flaw" OR "exploit" OR "attack") '
            'AND TITLE-ABS-KEY("cause*" OR "factor*" OR "source*")'
        ),
    },
    {
        "rq": "RQ4",
        "description": (
            "What strategies are used to mitigate vulnerabilities in RESTful APIs?"
        ),
        "change": "Interface block widened; filters made explicit.",
        "scopus": _scopus(
            API_SCOPUS,
            'vulnerabilit* OR "security threat*" OR attack*',
            '"mitigation strateg*" OR "security framework*" OR "defense mechanis*" '
            'OR "vulnerability management" OR "risk reduction" OR countermeasure* '
            'OR "hardening technique*" OR "secure design" OR "security control*"',
        ),
        "wos": _wos(
            API_WOS,
            'vulnerabilit* OR "security threat*" OR attack*',
            '"mitigation strateg*" OR "security framework*" OR "defense mechanis*" '
            'OR "vulnerability management" OR "risk reduction" OR countermeasure* '
            'OR "hardening technique*" OR "secure design" OR "security control*"',
        ),
        "legacy_scopus": (
            'TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TITLE-ABS-KEY(vulnerabilit* OR "security threat*" OR "attack*") '
            'AND TITLE-ABS-KEY("mitigation strateg*" OR "security framework*" '
            'OR "defense mechanis*" OR "vulnerability management" OR "risk reduction" '
            'OR "countermeasure*" OR "hardening technique*" OR "secure design")'
        ),
    },
    {
        "rq": "RQ5",
        "description": (
            "What are the most common security misconfigurations encountered "
            "during the development of RESTful APIs?"
        ),
        "change": (
            "A security block is now required. The original query paired "
            "configuration* with development*, both generic enough that any "
            "paper mentioning a REST API and its deployment matched; this is "
            "the query that admitted the largest share of off-topic records."
        ),
        "scopus": _scopus(
            API_SCOPUS,
            '"security misconfiguration*" OR misconfigur* OR "insecure configuration*" '
            'OR "security configuration*" OR "hardening"',
            "securit* OR vulnerabilit* OR exposure* OR attack*",
        ),
        "wos": _wos(
            API_WOS,
            '"security misconfiguration*" OR misconfigur* OR "insecure configuration*" '
            'OR "security configuration*" OR hardening',
            "securit* OR vulnerabilit* OR exposure* OR attack*",
        ),
        "legacy_scopus": (
            'TITLE-ABS-KEY("RESTful API" OR "REST API") '
            'AND TITLE-ABS-KEY("securit* misconfiguration*" OR configuration*) '
            "AND TITLE-ABS-KEY(development* OR SDLC OR DevOps OR DevSecOps OR standar*)"
        ),
    },
]
