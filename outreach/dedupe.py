#!/usr/bin/env python3
"""
Dedupe prospects against contacted_log.csv so the same roofing company never
gets an outreach message generated twice.

Matches on business_name, instagram_handle, and facebook_page_url (normalized,
case-insensitive) — a match on ANY one of those counts as "already contacted".

Does not touch Instagram or Facebook in any way; it only compares CSV rows.
"""

import argparse
import csv
import re
from pathlib import Path


def _normalize_handle(handle: str) -> str:
    return re.sub(r"^@", "", (handle or "").strip().lower())


def _normalize_url(url: str) -> str:
    url = (url or "").strip().lower()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url.rstrip("/")


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def prospect_keys(row: dict) -> set:
    """Identifying keys for a prospect row. Matching any one against the log counts as contacted."""
    keys = set()
    if row.get("business_name"):
        keys.add(("name", _normalize_name(row["business_name"])))
    if row.get("instagram_handle"):
        keys.add(("ig", _normalize_handle(row["instagram_handle"])))
    if row.get("facebook_page_url"):
        keys.add(("fb", _normalize_url(row["facebook_page_url"])))
    return keys


def load_contacted_keys(log_path: Path) -> set:
    keys = set()
    if not log_path.exists():
        return keys
    with log_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            keys |= prospect_keys(row)
    return keys


def is_contacted(row: dict, contacted_keys: set) -> bool:
    return bool(prospect_keys(row) & contacted_keys)


def filter_new_prospects(prospects_path: Path, log_path: Path):
    """Return (new_rows, skipped_rows) as lists of dicts, in original CSV order."""
    contacted_keys = load_contacted_keys(log_path)
    new_rows, skipped_rows = [], []
    with prospects_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if is_contacted(row, contacted_keys):
                skipped_rows.append(row)
            else:
                new_rows.append(row)
    return new_rows, skipped_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prospects_csv", nargs="?", default="outreach/prospects.csv")
    parser.add_argument("contacted_log_csv", nargs="?", default="outreach/contacted_log.csv")
    args = parser.parse_args()

    new_rows, skipped_rows = filter_new_prospects(Path(args.prospects_csv), Path(args.contacted_log_csv))

    print(f"{len(new_rows)} new prospect(s), {len(skipped_rows)} already contacted (skipped):")
    for row in skipped_rows:
        print(f"  - {row.get('business_name', '(unknown)')}")


if __name__ == "__main__":
    main()
