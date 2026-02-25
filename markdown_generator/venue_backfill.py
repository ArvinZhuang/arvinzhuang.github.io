#!/usr/bin/env python3
"""Fetch exact venue strings from Google Scholar and update _data/publications.yml.

Usage:
    python markdown_generator/venue_backfill.py --dry-run --verbose
    python markdown_generator/venue_backfill.py --use-proxy --delay 10 --verbose
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

SCHOLAR_ID = "-7sbXNIAAAAJ"
DEFAULT_DELAY = 5

# Short abbreviation to append in parens after the full name.
# Keys must match the exact strings Google Scholar returns.
VENUE_ABBREV = {
    "Proceedings of the Annual International ACM SIGIR Conference": "SIGIR",
    "SIGIR": "SIGIR",
    "ECIR": "ECIR",
    "European Conference on Information Retrieval": "ECIR",
    "EMNLP": "EMNLP",
    "Empirical Methods in Natural Language Processing": "EMNLP",
    "ACL": "ACL",
    "Association for Computational Linguistics": "ACL",
    "NAACL": "NAACL",
    "ICTIR": "ICTIR",
    "Theory of Information Retrieval": "ICTIR",
    "WSDM": "WSDM",
    "CIKM": "CIKM",
    "WWW": "WWW",
    "Web Conference": "WWW",
    "KDD": "KDD",
    "ICLR": "ICLR",
    "NeurIPS": "NeurIPS",
    "ICML": "ICML",
    "AAAI": "AAAI",
    "IJCAI": "IJCAI",
    "ACM Transactions on Information Systems": "TOIS",
    "TOIS": "TOIS",
    "Information Retrieval Journal": "IRJ",
    "International Journal on Digital Libraries": "IJDL",
    "ADCS": "ADCS",
    "Australasian Document Computing": "ADCS",
    "COLING": "COLING",
    "EACL": "EACL",
    "TREC": "TREC",
    "Text Retrieval Conference": "TREC",
    "SIGIR-AP": "SIGIR-AP",
    "SIGIR Forum": "SIGIR Forum",
}

# These venue strings need no abbreviation appended
NO_ABBREV = {"arXiv", "SIGIR Forum", "SIGIR-AP"}


def normalize_title(title: str) -> str:
    title = title.lower()
    title = title.translate(str.maketrans("", "", string.punctuation))
    return " ".join(title.split())


def get_abbrev(venue: str) -> str | None:
    """Return abbreviation for a venue string, or None if not needed."""
    if not venue or venue in NO_ABBREV:
        return None
    for substring, abbrev in VENUE_ABBREV.items():
        if substring.lower() in venue.lower():
            if f"({abbrev})" not in venue:
                return abbrev
    return None


def format_venue(venue: str) -> str:
    """Append (ABBREV) if not already present."""
    if not venue:
        return venue
    abbrev = get_abbrev(venue)
    if abbrev:
        return f"{venue} ({abbrev})"
    return venue


def load_publications(yml_path: Path) -> list[dict]:
    if not yml_path.exists():
        return []
    with open(yml_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def save_publications(yml_path: Path, entries: list[dict]) -> None:
    entries.sort(key=lambda e: (-e["year"], e["title"]))

    class OrderedDumper(yaml.SafeDumper):
        pass

    def represent_dict(dumper, data):
        return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())

    OrderedDumper.add_representer(dict, represent_dict)
    with open(yml_path, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, Dumper=OrderedDumper, default_flow_style=False,
                  allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(
        description="Backfill venue strings from Google Scholar into publications.yml."
    )
    parser.add_argument("--scholar-id", default=SCHOLAR_ID)
    parser.add_argument("--data-file", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--use-proxy", action="store_true")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    args = parser.parse_args()

    if args.data_file:
        yml_path = Path(args.data_file)
    else:
        script_dir = Path(__file__).resolve().parent
        yml_path = script_dir.parent / "_data" / "publications.yml"

    if args.verbose:
        print(f"Data file: {yml_path}")

    if args.use_proxy:
        pg = ProxyGenerator()
        scraper_api_key = os.environ.get("SCRAPER_API_KEY")
        if scraper_api_key:
            pg.ScraperAPI(scraper_api_key)
            if args.verbose:
                print("Using ScraperAPI proxy")
        else:
            pg.FreeProxies()
            if args.verbose:
                print("Using free proxies")
        scholarly.use_proxy(pg)

    data = load_publications(yml_path)
    norm_to_entry = {normalize_title(e["title"]): e for e in data}

    if args.verbose:
        print(f"Loaded {len(data)} existing publications")
        print(f"Fetching author profile for Scholar ID: {args.scholar_id}")

    author = scholarly.search_author_id(args.scholar_id)
    author = scholarly.fill(author, sections=["publications"])
    pubs = author.get("publications", [])
    total = len(pubs)
    if args.verbose:
        print(f"Found {total} publications on Scholar")

    updated = 0
    for i, pub_stub in enumerate(pubs, 1):
        stub_title = pub_stub.get("bib", {}).get("title", "").strip()
        norm = normalize_title(stub_title)
        if norm not in norm_to_entry:
            if args.verbose:
                print(f"  [{i}/{total}] SKIP (not in data): {stub_title[:55]}")
            if i < total:
                time.sleep(args.delay)
            continue

        if args.verbose:
            print(f"  [{i}/{total}] Filling: {stub_title[:55]}")
        try:
            pub = scholarly.fill(pub_stub)
        except Exception as e:
            if args.verbose:
                print(f"    WARNING: fill failed: {e}")
            if i < total:
                time.sleep(args.delay)
            continue

        bib = pub.get("bib", {})
        venue_raw = (bib.get("venue") or bib.get("journal") or
                     bib.get("conference") or "")
        if not venue_raw:
            if args.verbose:
                print("    (no venue returned)")
            if i < total:
                time.sleep(args.delay)
            continue

        venue = format_venue(venue_raw)
        entry = norm_to_entry[norm]

        if args.dry_run:
            print(f"  WOULD SET venue: {venue}")
        else:
            entry["venue"] = venue
            if args.verbose:
                print(f"    venue: {venue}")
            updated += 1

        if i < total:
            time.sleep(args.delay)

    if not args.dry_run and updated > 0:
        save_publications(yml_path, data)

    print(f"\nDone. {'Would update' if args.dry_run else 'Updated'} {updated} venue(s).")


if __name__ == "__main__":
    main()
