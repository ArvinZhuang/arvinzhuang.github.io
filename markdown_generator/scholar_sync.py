#!/usr/bin/env python3
"""Fetch publications from Google Scholar and generate Jekyll markdown files.

Usage:
    python markdown_generator/scholar_sync.py --dry-run --verbose
    python markdown_generator/scholar_sync.py
    python markdown_generator/scholar_sync.py --use-proxy --delay 10
"""

from __future__ import annotations

import argparse
import os
import re
import string
import time
import unicodedata
import yaml
from pathlib import Path
from typing import Optional

from scholarly import scholarly, ProxyGenerator

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCHOLAR_ID = "-7sbXNIAAAAJ"
AUTHOR_NAME = "Shengyao Zhuang"
DEFAULT_TRACK = "Full paper"
DEFAULT_DELAY = 5  # seconds between Scholar requests

# Mapping from substrings found in Scholar venue strings to abbreviations used
# in filenames and permalinks.  Order matters – first match wins.
VENUE_ABBREVIATION_MAP = [
    ("SIGIR-AP", "SIGIRAP"),
    ("SIGIR Forum", "SIGIR"),
    ("SIGIR", "SIGIR"),
    ("ECIR", "ECIR"),
    ("EMNLP", "EMNLP"),
    ("Association for Computational Linguistics", "ACL"),
    ("ACL", "ACL"),
    ("NAACL", "NAACL"),
    ("ICTIR", "ICTIR"),
    ("WSDM", "WSDM"),
    ("CIKM", "CIKM"),
    ("WWW", "WWW"),
    ("KDD", "KDD"),
    ("ICLR", "ICLR"),
    ("NeurIPS", "NeurIPS"),
    ("ICML", "ICML"),
    ("AAAI", "AAAI"),
    ("IJCAI", "IJCAI"),
    ("TOIS", "TOIS"),
    ("Transactions on Information Systems", "TOIS"),
    ("Information Retrieval Journal", "IRJ"),
    ("International Journal on Digital Libraries", "IJDL"),
    ("ADCS", "ADCS"),
    ("COLING", "COLING"),
    ("EACL", "EACL"),
    ("TREC", "TREC"),
    ("Natural Language Processing", "NLP"),
    ("arXiv", "arxiv"),
]

# Words to skip when building a shortname from the title
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "had", "has", "have", "he", "her", "his", "how", "if", "in", "into",
    "is", "it", "its", "not", "of", "on", "or", "our", "s", "she", "so",
    "than", "that", "the", "their", "them", "then", "there", "these",
    "they", "this", "to", "was", "we", "were", "what", "when", "where",
    "which", "while", "who", "will", "with", "you", "your",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def normalize_title(title: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    title = title.lower()
    title = title.translate(str.maketrans("", "", string.punctuation))
    title = " ".join(title.split())
    return title


def load_existing_publications(pub_dir: Path) -> set[str]:
    """Return a set of normalized titles from existing _publications/*.md."""
    titles: set[str] = set()
    for md_file in sorted(pub_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        # Extract YAML front matter between first pair of ---
        match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            continue
        try:
            front = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if front and "title" in front:
            titles.add(normalize_title(str(front["title"])))
    return titles


def extract_venue_abbreviation(venue: str) -> str:
    """Map a Scholar venue string to a short abbreviation for filenames."""
    if not venue:
        return "arxiv"
    for substring, abbrev in VENUE_ABBREVIATION_MAP:
        if substring.lower() in venue.lower():
            return abbrev
    # Try to find a parenthesized abbreviation, e.g. "(VENUE '24)"
    paren = re.search(r"\(([A-Z][A-Za-z0-9-]+)", venue)
    if paren:
        return paren.group(1).rstrip("'")
    return "arxiv"


def generate_shortname(title: str) -> str:
    """Generate a short identifier from the paper title.

    Prefers an explicit name before a colon (e.g. "TILDE: ...", "Rank-r1: ..."),
    then looks for all-caps acronyms, then falls back to PascalCase words.
    """
    # 1. Look for "Name:" pattern at the start — catches "TILDE:", "Rank-r1:",
    #    "FeB4RAG:", "Visa:", "R2LLMs:", etc.
    colon_match = re.match(r"^([A-Za-z0-9][\w-]{0,15}):\s", title)
    if colon_match:
        name = colon_match.group(1)
        # Clean up: remove trailing lowercase 's' from plurals like "R2LLMs"
        # and strip hyphens/underscores for use in filenames
        name = re.sub(r"s$", "", name) if re.search(r"[A-Z]s$", name) else name
        return name.replace("_", "")

    # 2. Look for an all-caps acronym (2+ uppercase chars, possibly with digits)
    acronym = re.search(r"\b([A-Z][A-Z0-9]{1,}(?:-[A-Z0-9]+)*)\b", title)
    if acronym:
        return acronym.group(1)

    # 3. Fallback: PascalCase first 2-3 significant words
    words = [w for w in re.findall(r"[A-Za-z]+", title) if w.lower() not in STOPWORDS]
    if not words:
        words = re.findall(r"[A-Za-z]+", title)
    chosen = words[:3]
    return "".join(w.capitalize() for w in chosen)


def format_authors(authors_str: str, highlight_name: str = AUTHOR_NAME) -> str:
    """Wrap the highlighted author name in <strong> tags.

    Matches by last-name + first-initial to handle cases where Scholar
    abbreviates first names (e.g. "S Zhuang" or "S. Zhuang").
    """
    if not authors_str:
        return ""

    parts = highlight_name.split()
    if len(parts) >= 2:
        first_name = parts[0]
        last_name = parts[-1]
    else:
        first_name = ""
        last_name = highlight_name

    # Patterns to match: full name, abbreviated, or initial
    patterns = [
        re.escape(highlight_name),  # "Shengyao Zhuang"
        re.escape(f"{first_name[0]}. {last_name}") if first_name else None,  # "S. Zhuang"
        re.escape(f"{first_name[0]} {last_name}") if first_name else None,   # "S Zhuang"
    ]
    patterns = [p for p in patterns if p]

    result = authors_str
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        if regex.search(result):
            result = regex.sub(f"<strong>{highlight_name}</strong>", result)
            break

    return result


def make_filename(year: int, venue_abbrev: str, shortname: str) -> str:
    """Build a filename like 2024-SIGIR-TILDE.md."""
    return f"{year}-{venue_abbrev}-{shortname}.md"


def make_permalink(venue_abbrev: str, year: int, shortname: str) -> str:
    """Build a permalink like /publication/SIGIR2024TILDE."""
    return f"/publication/{venue_abbrev}{year}{shortname}"


def build_markdown(pub: dict) -> str:
    """Build the full markdown string for a publication entry."""
    title = pub["title"]
    year = pub["year"]
    venue = pub["venue"]
    authors = pub["authors"]
    abstract = pub.get("abstract", "")
    url = pub.get("url", "")
    venue_abbrev = pub["venue_abbrev"]
    shortname = pub["shortname"]
    permalink = make_permalink(venue_abbrev, year, shortname)

    # YAML front matter — use the same quoting style as existing files
    lines = [
        "---",
        f'title: "{title}"',
        "collection: publications",
        f"permalink: {permalink}",
        f"year: {year}",
        f"venue: '{venue}'",
        f"authors: {authors}",
        f"track: {DEFAULT_TRACK}",
        "---",
        "---",
        "",
    ]

    if abstract:
        lines.append("## Abstract")
        lines.append(abstract)
        lines.append("")

    if url:
        lines.append(f"[Download paper here]({url})")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scholar fetching
# ---------------------------------------------------------------------------


def fetch_scholar_publications(
    scholar_id: str,
    use_proxy: bool = False,
    scraper_api_key: str | None = None,
    delay: float = DEFAULT_DELAY,
    verbose: bool = False,
) -> list[dict]:
    """Fetch all publications for the given Scholar author ID."""

    if use_proxy:
        pg = ProxyGenerator()
        if scraper_api_key:
            pg.ScraperAPI(scraper_api_key)
            if verbose:
                print("Using ScraperAPI proxy")
        else:
            pg.FreeProxies()
            if verbose:
                print("Using free proxies")
        scholarly.use_proxy(pg)

    if verbose:
        print(f"Fetching author profile for Scholar ID: {scholar_id}")

    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["publications"])

    publications = []
    total = len(author.get("publications", []))
    for i, pub_stub in enumerate(author.get("publications", []), 1):
        if verbose:
            print(f"  [{i}/{total}] Filling: {pub_stub.get('bib', {}).get('title', '???')}")

        try:
            pub = scholarly.fill(pub_stub)
        except Exception as e:
            if verbose:
                print(f"    WARNING: could not fill publication: {e}")
            pub = pub_stub

        bib = pub.get("bib", {})
        title = bib.get("title", "").strip()
        if not title:
            continue

        authors_raw = bib.get("author", "")
        if isinstance(authors_raw, list):
            authors_raw = ", ".join(authors_raw)
        # Scholar sometimes uses "and" as separator
        authors_raw = authors_raw.replace(" and ", ", ")
        # Clean up double commas
        authors_raw = re.sub(r",\s*,", ",", authors_raw).strip().rstrip(",")

        year = bib.get("pub_year", "")
        try:
            year = int(year)
        except (ValueError, TypeError):
            year = 0

        venue = bib.get("venue", "") or bib.get("journal", "") or bib.get("conference", "") or ""
        abstract = bib.get("abstract", "")

        # Try to get a URL
        url = pub.get("pub_url", "") or pub.get("eprint_url", "") or ""

        publications.append({
            "title": title,
            "authors_raw": authors_raw,
            "year": year,
            "venue_raw": venue,
            "abstract": abstract,
            "url": url,
        })

        if delay and i < total:
            time.sleep(delay)

    return publications


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Sync publications from Google Scholar to Jekyll markdown files."
    )
    parser.add_argument(
        "--scholar-id", default=SCHOLAR_ID,
        help=f"Google Scholar author ID (default: {SCHOLAR_ID})",
    )
    parser.add_argument(
        "--publications-dir", default=None,
        help="Path to _publications/ directory (default: auto-detect)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--verbose", action="store_true", help="Print detailed progress")
    parser.add_argument("--use-proxy", action="store_true", help="Use proxy for Scholar requests")
    parser.add_argument(
        "--delay", type=float, default=DEFAULT_DELAY,
        help=f"Delay in seconds between Scholar requests (default: {DEFAULT_DELAY})",
    )

    args = parser.parse_args()

    # Resolve publications directory
    if args.publications_dir:
        pub_dir = Path(args.publications_dir)
    else:
        # Assume script is in markdown_generator/ alongside _publications/
        script_dir = Path(__file__).resolve().parent
        pub_dir = script_dir.parent / "_publications"

    if not pub_dir.is_dir():
        print(f"ERROR: publications directory not found: {pub_dir}")
        raise SystemExit(1)

    if args.verbose:
        print(f"Publications directory: {pub_dir}")

    # Step 1: Load existing publications
    existing_titles = load_existing_publications(pub_dir)
    if args.verbose:
        print(f"Found {len(existing_titles)} existing publications")

    # Step 2: Fetch from Scholar
    scraper_api_key = os.environ.get("SCRAPER_API_KEY")
    pubs = fetch_scholar_publications(
        scholar_id=args.scholar_id,
        use_proxy=args.use_proxy,
        scraper_api_key=scraper_api_key,
        delay=args.delay,
        verbose=args.verbose,
    )
    if args.verbose:
        print(f"Fetched {len(pubs)} publications from Scholar")

    # Collect existing filenames to avoid collisions
    existing_filenames = {f.name for f in pub_dir.glob("*.md")}

    # Step 3: Filter and generate
    new_count = 0
    for pub in pubs:
        norm_title = normalize_title(pub["title"])
        if norm_title in existing_titles:
            if args.verbose:
                print(f"  SKIP (exists): {pub['title']}")
            continue

        if pub["year"] == 0:
            if args.verbose:
                print(f"  SKIP (no year): {pub['title']}")
            continue

        venue_abbrev = extract_venue_abbreviation(pub["venue_raw"])
        shortname = generate_shortname(pub["title"])
        authors = format_authors(pub["authors_raw"])

        pub_data = {
            "title": pub["title"],
            "year": pub["year"],
            "venue": pub["venue_raw"] or "Preprint",
            "authors": authors,
            "abstract": pub["abstract"],
            "url": pub["url"],
            "venue_abbrev": venue_abbrev,
            "shortname": shortname,
        }

        filename = make_filename(pub["year"], venue_abbrev, shortname)
        # Avoid filename collisions
        if filename in existing_filenames:
            for suffix in range(2, 100):
                candidate = make_filename(pub["year"], venue_abbrev, f"{shortname}{suffix}")
                if candidate not in existing_filenames:
                    filename = candidate
                    pub_data["shortname"] = f"{shortname}{suffix}"
                    break

        existing_filenames.add(filename)
        filepath = pub_dir / filename
        content = build_markdown(pub_data)

        if args.dry_run:
            print(f"  WOULD CREATE: {filename}")
            if args.verbose:
                print(f"    Title: {pub['title']}")
                print(f"    Year: {pub['year']}")
                print(f"    Venue: {pub['venue_raw']}")
                print(f"    Authors: {authors}")
                print(f"    Permalink: {make_permalink(venue_abbrev, pub['year'], shortname)}")
                print()
        else:
            filepath.write_text(content, encoding="utf-8")
            print(f"  CREATED: {filename}")

        new_count += 1

    print(f"\nDone. {'Would create' if args.dry_run else 'Created'} {new_count} new publication(s).")


if __name__ == "__main__":
    main()
