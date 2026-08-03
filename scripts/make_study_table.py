#!/usr/bin/env python3
"""Build the PRISMA item 17 study-characteristics appendix.

Reads the unified SLR corpus (``biblio_output/corpus_unificado.csv``) and emits a
LaTeX ``longtable`` with one row per DISTINCT primary study.  The CSV stores one
row per (study, research question) assignment, so a study assigned to two
research questions appears twice; such records are merged into a single row that
lists both questions.

Columns: running number, authors (first author, or both surnames for a pair, or
"first author et al." beyond two), year, short venue, research question(s), DOI.

Nothing is invented: where the source record carries no DOI, no venue, or no
author list, the corresponding cell is left empty.

Usage::

    python3 make_study_table.py [--csv PATH] [--out PATH] [--report]
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CSV = HERE / "biblio_output" / "corpus_unificado.csv"
DEFAULT_OUT = (
    HERE.parent.parent
    / "phd-thesis-document"
    / "9-appendices"
    / "B-CorpusTable.tex"
)

# --------------------------------------------------------------------------
# LaTeX escaping
# --------------------------------------------------------------------------

# Order matters: the backslash has to be handled before anything that inserts
# backslashes of its own.
_ESCAPES = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]

# Non-ASCII characters that appear in author and venue names.  The thesis
# compiles with pdflatex + inputenc(utf8) + fontenc(T1), which handles Latin-1
# and Latin Extended-A directly; anything outside that range is transliterated
# so the build never fails on a missing glyph.
_SAFE_UNICODE = re.compile(r"[\u0000-\u017F\u0192\u01FA-\u01FF\u1E00-\u1EFF]")


def strip_latex_markup(text: str) -> str:
    """Undo BibTeX-style accent markup found in some imported author strings.

    ``Ruiz-Cort{\\'e}s`` becomes ``Ruiz-Cortés`` before the value is re-escaped
    for output, so accents survive without a stray brace group.
    """
    if "{" not in text and "\\" not in text:
        return text
    accents = {
        "'": "\u0301", "`": "\u0300", '"': "\u0308", "^": "\u0302",
        "~": "\u0303", "c": "\u0327", "=": "\u0304", ".": "\u0307",
        "u": "\u0306", "v": "\u030C", "H": "\u030B", "r": "\u030A",
    }
    def repl(m: re.Match) -> str:
        acc, letter = m.group(1), m.group(2)
        combining = accents.get(acc)
        if combining is None:
            return letter
        return unicodedata.normalize("NFC", letter + combining)

    out = text
    # {\'e}, \'{e}, \'e  and the same with the other accent commands
    out = re.sub(r"\{\\([`'\"^~=.cuvHr])\{?([A-Za-z])\}?\}", repl, out)
    out = re.sub(r"\\([`'\"^~=.cuvHr])\{([A-Za-z])\}", repl, out)
    out = re.sub(r"\\([`'\"^~=.cuvHr])([A-Za-z])", repl, out)
    out = out.replace("{", "").replace("}", "")
    return out


def tex_escape(text: str) -> str:
    """Escape LaTeX special characters and normalize exotic Unicode."""
    if not text:
        return ""
    text = html.unescape(text)          # "Materials &amp; Continua"
    text = strip_latex_markup(text)
    text = unicodedata.normalize("NFC", text)
    # Typographic characters that inputenc maps poorly or that read badly in a
    # narrow table cell.
    for src, dst in (
        ("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'),
        ("\u2013", "--"), ("\u2014", "--"), ("\u2026", "..."),
        ("\u00a0", " "), ("\u2212", "-"),
    ):
        text = text.replace(src, dst)
    for src, dst in _ESCAPES:
        text = text.replace(src, dst)
    # Transliterate whatever the T1 encoding cannot render, without dropping a
    # letter: characters that decompose to nothing get an explicit fallback.
    fallback = {"ə": "a", "ǎ": "a", "Ǐ": "i", "ǐ": "i",
                "ı": "i", "İ": "I", "đ": "d", "Đ": "D",
                "ð": "d", "þ": "th", "ł": "l", "Ł": "L"}
    out = []
    for ch in text:
        if _SAFE_UNICODE.match(ch):
            out.append(ch)
            continue
        folded = unicodedata.normalize("NFKD", ch)
        folded = "".join(c for c in folded if not unicodedata.combining(c))
        folded = folded.encode("ascii", "ignore").decode("ascii")
        out.append(folded or fallback.get(ch, ""))
    return "".join(out).strip()


# --------------------------------------------------------------------------
# Author parsing
# --------------------------------------------------------------------------

_INITIALS = re.compile(r"^(?:[A-Z\u00C0-\u024F]\.){1,4}$")

# Two surnames reached the merged corpus with characters lost by the indexing
# service's export (Turkish dotless i rendered as "l", Romanian a-breve rendered
# as schwa).  Each replacement was checked against the record's own DOI through
# Crossref content negotiation; no name is corrected without that check.
AUTHOR_FIXES = {
    "Ylldlrlm": "Y\u0131ld\u0131r\u0131m",   # 10.1145/3655693.3655701
    "Dasc\u0259lu": "Dascalu",                # 10.12753/2066-026X-21-107
}


def _surname(entry: str) -> str:
    """Extract the surname from one author entry.

    Three storage conventions coexist in the merged corpus:

    * ``"S., Salva, Sebastien"``  (Scopus: initials, surname, given name)
    * ``"Dooley, R."``            (surname, initials)
    * ``"Alonso, Juan C."``       (surname, given name)

    The first is recognized by a leading initials-only token, in which case the
    surname is the second field; otherwise the surname is the first field.
    """
    parts = [p.strip() for p in entry.split(",") if p.strip()]
    if not parts:
        return ""
    name = parts[1] if (len(parts) >= 3
                        and _INITIALS.match(parts[0].replace(" ", ""))) else parts[0]
    return AUTHOR_FIXES.get(name, name)


def split_authors(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    entries = re.split(r"\s+and\s+", raw) if " and " in raw else raw.split(";")
    # Some source records truncate a co-author list with a literal "and others".
    # Splitting on " and " turns that into a surname, so drop it.
    drop = {"others", "other", "et al", "et al."}
    return [s for s in (_surname(e) for e in entries)
            if s and s.strip().lower().rstrip(".") not in drop]


def format_authors(raw: str) -> str:
    """First author plus ``et al.`` beyond two; both surnames for a pair."""
    surnames = split_authors(raw)
    if not surnames:
        return ""
    if len(surnames) == 1:
        return tex_escape(surnames[0])
    if len(surnames) == 2:
        return f"{tex_escape(surnames[0])} and {tex_escape(surnames[1])}"
    return tex_escape(surnames[0]) + r" \textit{et al.}"


def sort_key(record: dict) -> tuple:
    surnames = split_authors(record["Authors"])
    # Records without an author list sort last rather than first.
    lead = surnames[0].lower() if surnames else "\uffff"
    lead = "".join(
        c for c in unicodedata.normalize("NFKD", lead)
        if not unicodedata.combining(c)
    )
    try:
        year = int(record["Year"])
    except (TypeError, ValueError):
        year = 0
    return (lead, year, record["Title"].lower())


# --------------------------------------------------------------------------
# Venue shortening
# --------------------------------------------------------------------------

VENUE_SHORT = {
    "acm transactions on multimedia computing, communications and applications": "ACM TOMM",
    "acm transactions on software engineering and methodology": "ACM TOSEM",
    "acm conference proceedings": "ACM Conf. Proc.",
    "acm international conference proceeding series": "ACM ICPS",
    "acm international workshop proceedings": "ACM Workshop Proc.",
    "advanced materials research": "Adv. Mater. Res.",
    "advances in intelligent systems and computing": "AISC",
    "applied sciences (switzerland)": "Appl. Sci.",
    "bmc bioinformatics": "BMC Bioinformatics",
    "ceur workshop proceedings": "CEUR Workshop Proc.",
    "cmes - computer modeling in engineering and sciences": "CMES",
    "cluster computing": "Cluster Comput.",
    "communications in computer and information science": "CCIS",
    "computer journal": "Comput. J.",
    "computers, materials & continua": "Comput. Mater. Contin.",
    "computers, materials and continua": "Comput. Mater. Contin.",
    "computing": "Computing",
    "electronics": "Electronics",
    "electronics (switzerland)": "Electronics",
    "empirical software engineering": "Empir. Softw. Eng.",
    "energies": "Energies",
    "future generation computer systems": "Future Gener. Comput. Syst.",
    "ieee access": "IEEE Access",
    "ieee transactions on network and service management": "IEEE TNSM",
    "ieee transactions on services computing": "IEEE TSC",
    "ieice transactions on information and systems": "IEICE Trans. Inf. Syst.",
    "iete journal of research": "IETE J. Res.",
    "indian journal of computer science and engineering": "Indian J. Comput. Sci. Eng.",
    "information management and computer security": "Inf. Manag. Comput. Secur.",
    "information sciences": "Inf. Sci.",
    "information and software technology": "Inf. Softw. Technol.",
    "international journal of computing and digital systems": "Int. J. Comput. Digit. Syst.",
    "international journal of engineering trends and technology": "Int. J. Eng. Trends Technol.",
    "international journal of innovative research and scientific studies": "Int. J. Innov. Res. Sci. Stud.",
    "international journal of parallel, emergent and distributed systems": "Int. J. Parallel Emerg. Distrib. Syst.",
    "international journal of reasoning-based intelligent systems": "Int. J. Reason. Intell. Syst.",
    "journal of supercomputing": "J. Supercomput.",
    "journal of theoretical and applied information technology": "J. Theor. Appl. Inf. Technol.",
    "ksii transactions on internet and information systems": "KSII Trans. Internet Inf. Syst.",
    "lecture notes in computer science": "LNCS",
    "lecture notes in information systems and organisation": "LNISO",
    "lecture notes in networks and systems": "LNNS",
    "lecture notes of the institute for computer sciences, social informatics and telecommunications engineering": "LNICST",
    "military technical courier/vojnotehnicki glasnik": "Vojnoteh. Glas.",
    "openaccess series in informatics": "OASIcs",
    "procedia cirp": "Procedia CIRP",
    "procedia computer science": "Procedia Comput. Sci.",
    "proceedings - ieee computer society's international computer software and applications conference": "COMPSAC",
    "proceedings - ieee global communications conference, globecom": "GLOBECOM",
    "proceedings - international conference on advanced information networking and applications, aina": "AINA",
    "proceedings - international conference on quality software": "QSIC",
    "proceedings - international conference on software engineering": "ICSE",
    "proceedings 2025 workshop on security and privacy of next-generation networks": "FutureG Workshop",
    "proceedings of science": "PoS",
    "proceedings of the 2019 27th acm joint meeting on european software engineering conference and symposium on the foundations of software engineering": "ESEC/FSE",
    "proceedings of the 2024 on acm sigsac conference on computer and communications security": "ACM CCS",
    "proceedings of the 44th international conference on software engineering": "ICSE",
    "proceedings of the acm on software engineering": "Proc. ACM Softw. Eng.",
    "proceedings of the international astronautical congress, iac": "IAC",
    "proceedings of the national conference on communications, ncc": "NCC",
    "revista iberoamericana de tecnologias del aprendizaje": "IEEE RITA",
    "sn computer science": "SN Comput. Sci.",
    "science of computer programming": "Sci. Comput. Program.",
    "sensors": "Sensors",
    "service oriented computing and applications": "Serv. Oriented Comput. Appl.",
    "social network analysis and mining": "Soc. Netw. Anal. Min.",
    "software": "Software",
    "software & systems modeling": "Softw. Syst. Model.",
    "studies in computational intelligence": "Stud. Comput. Intell.",
    "telematika": "Telematika",
    "the 27th international symposium on research in attacks, intrusions and defenses": "RAID",
    "tsinghua science and technology": "Tsinghua Sci. Technol.",
    "world journal of advanced research and reviews": "World J. Adv. Res. Rev.",
    "elearning and software for education conference": "eLSE",
    "2014 panhellenic conference on informatics": "PCI",
    "international conference on advanced communication technology, icact": "ICACT",
    "international conference on evaluation of novel approaches to software engineering, enase - proceedings": "ENASE",
    "international conference on human system interaction, hsi": "HSI",
    "international conference on information networking": "ICOIN",
    "ieee international conference on software testing, verification and validation (icst)": "ICST",
    "ieee/acm 47th international conference on software engineering": "ICSE",
}

# Generic word-level fallback for venues absent from the table above.
WORD_SHORT = {
    "international": "Int.", "conference": "Conf.", "proceedings": "Proc.",
    "proceeding": "Proc.", "series": "Ser.", "journal": "J.",
    "transactions": "Trans.", "software": "Softw.", "engineering": "Eng.",
    "computer": "Comput.", "computing": "Comput.", "computers": "Comput.",
    "science": "Sci.", "sciences": "Sci.", "systems": "Syst.", "system": "Syst.",
    "information": "Inf.", "technology": "Technol.", "technologies": "Technol.",
    "symposium": "Symp.", "applications": "Appl.", "application": "Appl.",
    "communications": "Commun.", "communication": "Commun.",
    "networks": "Netw.", "network": "Netw.", "networking": "Netw.",
    "research": "Res.", "advanced": "Adv.", "advances": "Adv.",
    "intelligent": "Intell.", "management": "Manag.", "security": "Secur.",
    "reliability": "Reliab.", "distributed": "Distrib.",
    "programming": "Program.", "modeling": "Model.", "empirical": "Empir.",
    "national": "Natl.", "annual": "Annu.", "digital": "Digit.",
    "innovative": "Innov.", "studies": "Stud.", "emergent": "Emerg.",
    "service": "Serv.", "services": "Serv.", "multimedia": "Multimed.",
    "methodology": "Methodol.", "verification": "Verif.",
    "validation": "Valid.", "testing": "Test.", "global": "Glob.",
    "society": "Soc.", "european": "Eur.", "foundations": "Found.",
    "quality": "Qual.", "education": "Educ.", "analysis": "Anal.",
    "electronics": "Electron.", "workshops": "Workshops",
}

# A trailing acronym in parentheses, optionally followed by a year: "(ICSE 2025)".
_PAREN_ACRONYM = re.compile(r"\(([A-Z][A-Za-z0-9/&+-]{1,14})(?:\s+\d{4})?\)\s*$")
# A trailing comma-separated acronym: "..., ENASE - Proceedings" or "..., HSI".
_TAIL_ACRONYM = re.compile(r",\s*([A-Z]{2,10})(?:\s*-\s*Proceedings)?\s*$")
_LEADING_NOISE = re.compile(
    r"^(?:\d{4}\s+)?(?:IEEE(?:/ACM)?|ACM(?:/IEEE)?\s)?\s*\d*(?:st|nd|rd|th)?\s*",
    re.IGNORECASE,
)


def short_venue(source_title: str, doc_type: str) -> str:
    raw = html.unescape((source_title or "").strip())
    if not raw:
        return ""
    low = raw.lower()
    if low.startswith("arxiv") or "preprint" in doc_type.lower():
        return "arXiv"
    if low in VENUE_SHORT:
        return VENUE_SHORT[low]
    m = _PAREN_ACRONYM.search(raw)
    if m:
        return m.group(1)
    m = _TAIL_ACRONYM.search(raw)
    if m:
        return m.group(1)
    trimmed = _LEADING_NOISE.sub("", raw).strip()
    words = []
    for w in (trimmed or raw).split():
        key = w.lower().strip(",")
        words.append(WORD_SHORT.get(key, w))
    return " ".join(words)


# --------------------------------------------------------------------------
# Corpus assembly
# --------------------------------------------------------------------------

_RQ = re.compile(r"^(RQ\d)")


def rq_label(value: str) -> str:
    m = _RQ.match((value or "").strip())
    return m.group(1) if m else ""


def load_studies(csv_path: Path) -> tuple[list[dict], int, int]:
    """Merge the per-assignment rows into one record per distinct study."""
    with csv_path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    merged: dict[str, dict] = {}
    for row in rows:
        key = " ".join(row["Title"].split()).lower()
        rq = rq_label(row.get("RQ", ""))
        if key in merged:
            if rq and rq not in merged[key]["rqs"]:
                merged[key]["rqs"].append(rq)
            # Prefer the more complete of two duplicate records field by field.
            for field in ("Authors", "Source title", "DOI", "Year"):
                if not merged[key][field].strip() and row.get(field, "").strip():
                    merged[key][field] = row[field]
            continue
        record = {f: (row.get(f) or "").strip() for f in
                  ("Authors", "Title", "Year", "Source title",
                   "Document Type", "DOI")}
        record["rqs"] = [rq] if rq else []
        merged[key] = record

    studies = sorted(merged.values(), key=sort_key)
    for study in studies:
        study["rqs"].sort()
    return studies, len(rows), sum(1 for r in rows if r["DOI"].strip())


PREAMBLE = r"""\chapter{Corpus of primary studies}
\label{app:corpus}

This appendix lists every primary study included in the systematic review of
\cref{chap:state-of-the-art}, in fulfillment of item 17 of the PRISMA 2020
statement. Each study carries a key of the form \texttt{S\emph{n}}, which
resolves in the primary-study bibliography deposited with the review artifact,
and each row reports the characteristics the item asks a review to present:
authors, title, year of publication, publication venue, research question
addressed, and Digital Object Identifier. The primary-study series is kept
separate from the bibliography of the thesis body because the corpus extends
beyond the works the argument cites.

The base is %(n_studies)d distinct primary studies carrying
%(n_rows)d question assignments: two studies contribute evidence to two research
questions at once and therefore appear once in the table with both labels in the
RQ column. Of the %(n_studies)d studies, %(n_doi)d carry a Digital Object
Identifier; the remaining %(n_nodoi)d are indexed without one, and their DOI cell is
left empty rather than filled with a substitute. Venue names are given in short
form, with \textit{arXiv} standing for a preprint. Every included study carries
a venue: the cells the unified corpus left empty were recovered from the
conference-name and abbreviated-title fields of the source exports and, where
those were silent, from the Digital Object Identifier registry. Titles are given in full;
where a source record truncated the title, the deposited artifact records the
truncation rather than repairing it silently. Studies are ordered by
first author and then by year of publication.

{\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.15}
\begin{longtable}{@{}l>{\raggedright\arraybackslash}p{0.15\textwidth}>{\raggedright\arraybackslash}p{0.30\textwidth}c>{\raggedright\arraybackslash}p{0.16\textwidth}l>{\raggedright\arraybackslash}p{0.20\textwidth}@{}}
\caption{Characteristics of the %(n_studies)d primary studies included in the
systematic literature review: authors, title, year of publication, publication
venue in short form, research question addressed, and Digital Object Identifier
where the source record provides one. The key in the first column resolves in
the primary-study bibliography of the deposited artifact.}
\label{tab:corpus_studies}\\
\toprule
\textbf{Key} & \textbf{Authors} & \textbf{Title} & \textbf{Year} & \textbf{Venue} & \textbf{RQ} & \textbf{DOI} \\
\midrule
\endfirsthead
\multicolumn{7}{@{}l}{\textit{\Cref{tab:corpus_studies} continued from the previous page.}}\\
\toprule
\textbf{Key} & \textbf{Authors} & \textbf{Title} & \textbf{Year} & \textbf{Venue} & \textbf{RQ} & \textbf{DOI} \\
\midrule
\endhead
\midrule
\multicolumn{7}{r@{}}{\textit{Continued on the next page.}}\\
\endfoot
\bottomrule
\endlastfoot
"""

POSTAMBLE = r"""\end{longtable}
}
"""


def emit(studies: list[dict], n_rows: int, n_doi: int) -> str:
    # The DOI count in the prose is over STUDIES, which is what the table lists;
    # counting over assignments would not reconcile with the printed row count.
    studies_with_doi = sum(1 for s in studies if s["DOI"].strip())
    header = PREAMBLE % {
        "n_studies": len(studies),
        "n_rows": n_rows,
        "n_doi": studies_with_doi,
        "n_nodoi": len(studies) - studies_with_doi,
    }
    lines = [header]
    for i, s in enumerate(studies, start=1):
        authors = format_authors(s["Authors"])
        title = tex_escape(s["Title"].strip())
        year = tex_escape(s["Year"])
        venue = tex_escape(short_venue(s["Source title"], s["Document Type"]))
        rqs = ", ".join(s["rqs"])
        doi = s["DOI"].strip()
        doi_cell = r"\nolinkurl{%s}" % doi if doi else ""
        lines.append(
            f"S{i} & {authors} & {title} & {year} & {venue} & {rqs} & {doi_cell} \\\\"
        )
    lines.append(POSTAMBLE)
    return "\n".join(lines) + "\n"


CONF_HINTS = ("conference", "proceedings", "symposium", "workshop", "congress")


def bib_authors(raw: str) -> str:
    """Normalize the three author formats the corpus carries into BibTeX form.

    Scopus exports use "I., Lastname, Firstname; ...", BibTeX-derived records
    use "Lastname, Firstname and ...", and a few records end in the "and others"
    artifact of a list truncated on import.
    """
    raw = (raw or "").strip()
    if not raw:
        return ""
    if " and " in raw and ";" not in raw:
        return raw
    names = []
    for part in (p.strip() for p in raw.split(";")):
        if not part:
            continue
        bits = [b.strip() for b in part.split(",") if b.strip()]
        # Scopus prefixes each name with its initials, "A.H., Al-Omari, Ahmad".
        # The initials group is one or more capitals each followed by a period,
        # so "A." and "A.H." both qualify and a surname never does.
        if len(bits) >= 3 and re.fullmatch(r"(?:[A-Z]\.)+", bits[0]):
            names.append(f"{bits[1]}, {bits[2]}")
        elif len(bits) >= 2:
            names.append(f"{bits[0]}, {bits[1]}")
        elif bits:
            names.append(bits[0])
    return " and ".join(names)


def emit_bib(studies: list[dict]) -> str:
    """Emit one BibTeX entry per study, keyed to match the table exactly.

    The keys are assigned from the same ordered list the table iterates, so
    row S17 and entry S17 are the same study by construction rather than by a
    sort that two scripts have to agree on.
    """
    out = [
        "% Primary studies of the systematic literature review.",
        "% Keys S1..Sn correspond row for row to the corpus appendix table.",
        f"% {len(studies)} studies. Generated by make_study_table.py.",
        "",
    ]
    for i, s in enumerate(studies, start=1):
        venue = (s.get("Source title") or "").strip()
        dt = (s.get("Document Type") or "").lower()
        is_conf = "conference" in dt or "proceedings" in dt or any(
            h in venue.lower() for h in CONF_HINTS
        )
        kind = "incollection" if "book" in dt else ("inproceedings" if is_conf else "article")
        field = "journal" if kind == "article" else "booktitle"

        lines = [f"@{kind}{{S{i},"]
        auth = bib_authors(s.get("Authors", ""))
        if auth:
            lines.append(f"  author    = {{{auth}}},")
        lines.append(f"  title     = {{{s['Title'].strip()}}},")
        if venue:
            lines.append(f"  {field:9s} = {{{venue}}},")
        else:
            lines.append("  note      = {Venue not recorded in the source database export},")
        if s.get("Year"):
            lines.append(f"  year      = {{{s['Year']}}},")
        if s.get("DOI", "").strip():
            lines.append(f"  doi       = {{{s['DOI'].strip()}}},")
        lines.append(f"  keywords  = {{{', '.join(s['rqs'])}}},")
        lines.append("}")
        out.append("\n".join(lines))
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--bib", type=Path, default=None,
                    help="also write the primary-study bibliography here")
    ap.add_argument("--report", action="store_true",
                    help="print corpus counts to stderr")
    args = ap.parse_args()

    studies, n_rows, n_doi = load_studies(args.csv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(emit(studies, n_rows, n_doi), encoding="utf-8")

    if args.bib:
        args.bib.parent.mkdir(parents=True, exist_ok=True)
        args.bib.write_text(emit_bib(studies), encoding="utf-8")
        print(f"wrote {args.bib}")

    if args.report:
        n_multi = sum(1 for s in studies if len(s["rqs"]) > 1)
        print(f"assignments (CSV rows) : {n_rows}", file=sys.stderr)
        print(f"distinct studies (rows): {len(studies)}", file=sys.stderr)
        print(f"studies in two RQs     : {n_multi}", file=sys.stderr)
        print(f"records with a DOI     : {n_doi}", file=sys.stderr)
        print(f"studies without authors: "
              f"{sum(1 for s in studies if not s['Authors'])}", file=sys.stderr)
        print(f"studies without venue  : "
              f"{sum(1 for s in studies if not s['Source title'])}",
              file=sys.stderr)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
