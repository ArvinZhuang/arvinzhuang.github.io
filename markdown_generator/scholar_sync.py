#!/usr/bin/env python3
"""Fetch publications from Google Scholar and sync to _data/publications.yml.

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
import yaml
from pathlib import Path

from scholarly import scholarly, ProxyGenerator

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCHOLAR_ID = "-7sbXNIAAAAJ"
AUTHOR_NAME = "Shengyao Zhuang"
DEFAULT_DELAY = 5  # seconds between Scholar requests

VENUE_ABBREVIATION_MAP = [
    ("SIGIR-AP", "SIGIR-AP"),
    ("SIGIR Forum", "SIGIR Forum"),
    ("SIGIR", "SIGIR"),
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
    ("ECIR", "ECIR"),
    ("TREC", "TREC"),
    ("arXiv", "arXiv"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def normalize_title(title: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    title = title.lower()
    title = title.translate(str.maketrans("", "", string.punctuation))
    title = " ".join(title.split())
    return title


def abbreviate_venue(venue: str) -> str:
    """Map a Scholar venue string to a short abbreviation."""
    if not venue:
        return "arXiv"
    for substring, abbrev in VENUE_ABBREVIATION_MAP:
        if substring.lower() in venue.lower():
            return abbrev
    return venue


def format_authors(authors_str: str, highlight_name: str = AUTHOR_NAME) -> str:
    """Wrap the highlighted author name in <strong> tags."""
    if not authors_str:
        return ""

    parts = highlight_name.split()
    if len(parts) >= 2:
        first_name = parts[0]
        last_name = parts[-1]
    else:
        first_name = ""
        last_name = highlight_name

    patterns = [
        re.escape(highlight_name),
        re.escape(f"{first_name[0]}. {last_name}") if first_name else None,
        re.escape(f"{first_name[0]} {last_name}") if first_name else None,
    ]
    patterns = [p for p in patterns if p]

    result = authors_str
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        if regex.search(result):
            result = regex.sub(f"<strong>{highlight_name}</strong>", result)
            break

    return result


def load_publications(yml_path: Path) -> list[dict]:
    """Load existing publications from YAML file."""
    if not yml_path.exists():
        return []
    with open(yml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or []


def save_publications(yml_path: Path, entries: list[dict]) -> None:
    """Sort by year desc then title asc, and write YAML."""
    entries.sort(key=lambda e: (-e["year"], e["title"]))

    class OrderedDumper(yaml.SafeDumper):
        pass

    def represent_dict(dumper, data):
        return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())

    OrderedDumper.add_representer(dict, represent_dict)

    yml_path.parent.mkdir(parents=True, exist_ok=True)
    with open(yml_path, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, Dumper=OrderedDumper, default_flow_style=False,
                  allow_unicode=True, sort_keys=False)


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
        authors_raw = authors_raw.replace(" and ", ", ")
        authors_raw = re.sub(r",\s*,", ",", authors_raw).strip().rstrip(",")

        year = bib.get("pub_year", "")
        try:
            year = int(year)
        except (ValueError, TypeError):
            year = 0

        url = pub.get("pub_url", "") or pub.get("eprint_url", "") or ""
        venue = bib.get("venue", "") or bib.get("journal", "") or bib.get("conference", "") or ""

        publications.append({
            "title": title,
            "authors_raw": authors_raw,
            "year": year,
            "venue_raw": venue,
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
        description="Sync publications from Google Scholar to _data/publications.yml."
    )
    parser.add_argument(
        "--scholar-id", default=SCHOLAR_ID,
        help=f"Google Scholar author ID (default: {SCHOLAR_ID})",
    )
    parser.add_argument(
        "--data-file", default=None,
        help="Path to publications.yml (default: auto-detect)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--verbose", action="store_true", help="Print detailed progress")
    parser.add_argument("--use-proxy", action="store_true", help="Use proxy for Scholar requests")
    parser.add_argument(
        "--delay", type=float, default=DEFAULT_DELAY,
        help=f"Delay in seconds between Scholar requests (default: {DEFAULT_DELAY})",
    )

    args = parser.parse_args()

    # Resolve data file path
    if args.data_file:
        yml_path = Path(args.data_file)
    else:
        script_dir = Path(__file__).resolve().parent
        yml_path = script_dir.parent / "_data" / "publications.yml"

    if args.verbose:
        print(f"Data file: {yml_path}")

    # Step 1: Load existing publications
    existing = load_publications(yml_path)
    existing_titles = {normalize_title(e["title"]) for e in existing}
    if args.verbose:
        print(f"Found {len(existing)} existing publications")

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

    # Step 3: Append new entries
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

        authors = format_authors(pub["authors_raw"])
        venue = abbreviate_venue(pub.get("venue_raw", ""))

        entry = {
            "title": pub["title"],
            "authors": authors,
            "year": pub["year"],
            "venue": venue,
        }
        if pub["url"]:
            entry["url"] = pub["url"]

        if args.dry_run:
            print(f"  WOULD ADD: {pub['title']} ({pub['year']})")
        else:
            existing.append(entry)
            existing_titles.add(norm_title)

        new_count += 1

    # Step 4: Write back
    if not args.dry_run and new_count > 0:
        save_publications(yml_path, existing)

    print(f"\nDone. {'Would add' if args.dry_run else 'Added'} {new_count} new publication(s).")


if __name__ == "__main__":
    main()
