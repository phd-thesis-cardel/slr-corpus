"""
Search queries for the 5 research questions, adapted per API.

Each query is a dict with:
  - rq: research question identifier (RQ1..RQ5)
  - openalex: query string for OpenAlex search API
  - scopus: query string for Scopus TITLE-ABS-KEY syntax
  - wos: query string for Web of Science TS= syntax (for future use)
"""

QUERIES = [
    {
        "rq": "RQ1",
        "description": "What mutation operators have been developed and used for testing the security of RESTful APIs?",
        "openalex": (
            '("mutation testing" OR "mutation analysis" OR "mutation operator" '
            'OR "software mutation" OR "program mutation" OR "mutant generation") '
            'AND (("REST" AND "API") OR "web API" OR "HTTP API" OR "cloud API") '
            'AND (security OR vulnerability OR privacy OR authorization OR authentication OR "access control")'
        ),
        "scopus": (
            'TITLE-ABS-KEY("mutation testing" OR "mutation operator*" OR "software mutation*" '
            'OR "program mutation*" OR "mutation analysis") '
            'AND TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TITLE-ABS-KEY("security*" OR "vulnerabilit*" OR "privac*")'
        ),
        "wos": (
            'TS=("mutation testing" OR "mutation operator*" OR "software mutation*" '
            'OR "program mutation*" OR "mutation analysis") '
            'AND TS=("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TS=("security*" OR vulnerabilit* OR privac*)'
        ),
    },
    {
        "rq": "RQ2",
        "description": "What limitations or challenges are associated with current mutation operators?",
        "openalex": (
            '("mutation testing" OR "mutation operator" OR "software mutation" '
            'OR "program mutation" OR "mutation analysis") '
            'AND ("REST API" OR "cloud API" OR "web API") '
            'AND (limitation OR challenge OR drawback OR issue)'
        ),
        "scopus": (
            'TITLE-ABS-KEY("mutation testing" OR "mutation operator*" OR "software mutation*" '
            'OR "program mutation*" OR "mutation analysis") '
            'AND TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TITLE-ABS-KEY(limitation* OR challenge* OR drawback* OR issue*)'
        ),
        "wos": (
            'TS=("mutation testing" OR "mutation operator*" OR "software mutation*" '
            'OR "program mutation*" OR "mutation analysis") '
            'AND TS=("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TS=(limitation* OR challenge* OR drawback* OR issue*)'
        ),
    },
    {
        "rq": "RQ3",
        "description": "What factors contribute to finding vulnerabilities in RESTful API services?",
        "openalex": (
            '("REST API" OR "cloud API" OR "web API") '
            'AND (vulnerability OR "security flaw" OR exploit OR attack) '
            'AND (cause OR factor OR source)'
        ),
        "scopus": (
            'TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TITLE-ABS-KEY("vulnerability" OR "security flaw" OR "exploit" OR "attack") '
            'AND TITLE-ABS-KEY("cause*" OR "factor*" OR "source*")'
        ),
        "wos": (
            'TS=("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TS=("vulnerability" OR "security flaw" OR "exploit" OR "attack") '
            'AND TS=("cause*" OR "factor*" OR "source*")'
        ),
    },
    {
        "rq": "RQ4",
        "description": "What strategies are used to mitigate vulnerabilities in RESTful APIs?",
        "openalex": (
            '("REST API" OR "cloud API" OR "web API") '
            'AND (vulnerability OR "security threat" OR attack) '
            'AND ("mitigation strategy" OR "security framework" OR "defense mechanism" '
            'OR "vulnerability management" OR "risk reduction" OR countermeasure '
            'OR "hardening technique" OR "secure design")'
        ),
        "scopus": (
            'TITLE-ABS-KEY("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TITLE-ABS-KEY(vulnerabilit* OR "security threat*" OR "attack*") '
            'AND TITLE-ABS-KEY("mitigation strateg*" OR "security framework*" OR "defense mechanis*" '
            'OR "vulnerability management" OR "risk reduction" OR "countermeasure*" '
            'OR "hardening technique*" OR "secure design")'
        ),
        "wos": (
            'TS=("REST* API*" OR "Cloud* API*" OR "Web API*") '
            'AND TS=(vulnerabilit* OR "security threat*" OR attack*) '
            'AND TS=("mitigation strateg*" OR "security framework*" OR "defense mechanis*" '
            'OR "vulnerability management" OR "risk reduction" OR "countermeasure*" '
            'OR "hardening technique*" OR "secure design")'
        ),
    },
    {
        "rq": "RQ5",
        "description": "What are the most common security misconfigurations encountered during the development of RESTful APIs?",
        "openalex": (
            '("RESTful API" OR "REST API") '
            'AND ("security misconfiguration" OR configuration) '
            'AND (development OR SDLC OR DevOps OR DevSecOps OR standard)'
        ),
        "scopus": (
            'TITLE-ABS-KEY("RESTful API" OR "REST API") '
            'AND TITLE-ABS-KEY("securit* misconfiguration*" OR configuration*) '
            'AND TITLE-ABS-KEY(development* OR SDLC OR DevOps OR DevSecOps OR standar*)'
        ),
        "wos": (
            'TS=("RESTful API" OR "REST API") '
            'AND TS=("securit* misconfiguration*" OR configuration*) '
            'AND TS=(development* OR SDLC OR DevOps OR DevSecOps OR standar*)'
        ),
    },
]
