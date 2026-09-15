#!/usr/bin/env python3
"""
Generate personalized IG/FB outreach copy for Cabren's roofing prospects.

Reads a prospects CSV, drops anyone already in contacted_log.csv, routes each
prospect to a primary service (AI Receptionist / AI Web Chat / Website Build),
and writes an output CSV with a personalized opener and two ready-to-send
message variants (friendly-local-peer tone) for A/B testing.

This script only writes text to a CSV. It never logs into, browses, scrapes,
or sends anything through Instagram or Facebook — you copy/paste and send the
messages yourself.
"""

import argparse
import csv
from pathlib import Path

from dedupe import filter_new_prospects

OUTPUT_COLUMNS = [
    "business_name",
    "primary_service",
    "opener",
    "message_variant_1",
    "message_variant_2",
    "status",
    "notes",
]

DEMO_LINE = "a quick live demo built for your business"

NO_SITE_VALUES = {"no site", "no website", "none", ""}
OUTDATED_VALUES = {"outdated"}
HAS_SITE_VALUES = {"has site", "has website"}

# Default routing (no extra ICP overrides given):
#   no site / outdated  -> Website Build (the core gap is the site itself)
#   has site, >=1000 followers -> AI Web Chat (already active in social/DM-style channels)
#   has site, <1000 followers  -> AI Receptionist (missed-call is the more universal pain point)
FOLLOWER_THRESHOLD_FOR_WEB_CHAT = 1000


def route_primary_service(row: dict) -> str:
    status = (row.get("website_status") or "").strip().lower()
    if status in NO_SITE_VALUES or status in OUTDATED_VALUES:
        return "Website Build"
    if status in HAS_SITE_VALUES:
        try:
            followers = int(str(row.get("follower_count", "0")).replace(",", "").strip() or 0)
        except ValueError:
            followers = 0
        return "AI Web Chat" if followers >= FOLLOWER_THRESHOLD_FOR_WEB_CHAT else "AI Receptionist"
    return "AI Receptionist"


def build_opener(row: dict) -> str:
    name = row.get("business_name", "").strip() or "there"
    city = row.get("city/state", "").strip()
    topic = row.get("recent_post_topic", "").strip()
    status = (row.get("website_status") or "").strip().lower()
    city_bit = f" ({city})" if city else ""

    if topic:
        return f"Hey! Saw your post about {topic} — looks like {name}'s been keeping busy."
    if status in NO_SITE_VALUES:
        return f"Hey! Came across {name}'s page{city_bit} and noticed you don't have a website up yet."
    if status in OUTDATED_VALUES:
        return f"Hey! Was checking out {name}'s page{city_bit} — noticed your website looks like it hasn't been touched in a while."
    return f"Hey! Came across {name}'s page{city_bit} and wanted to reach out."


# Each service has two distinct pitch phrasings (not just a swapped CTA) so the
# variants are genuinely different for reply-rate A/B testing.
PITCHES = {
    "Website Build": [
        "I build websites for roofing companies — fast, mobile-friendly, easy for people to book from. "
        f"I'll actually put together {DEMO_LINE} first, no cost, just so you can see it before we talk about anything else.",
        "I help roofers get a website that actually brings in calls instead of just sitting there. "
        f"I always build the demo first — {DEMO_LINE} — so you're seeing something real, not a sales pitch.",
    ],
    "AI Receptionist": [
        "I set up AI receptionists for roofing companies so no call goes unanswered, even nights and weekends when you're wrapped up on a job. "
        f"I build {DEMO_LINE} first, free, so you can hear exactly how it sounds before deciding anything.",
        "Curious if missed calls are costing you jobs — I build AI receptionists for roofers so every call gets picked up and estimates get booked automatically. "
        f"I always start with {DEMO_LINE}, no strings attached, so you can hear it for yourself.",
    ],
    "AI Web Chat": [
        "I build AI chat for roofing company pages so anyone who messages or visits gets booked for an estimate right away instead of going cold. "
        f"I'll put together {DEMO_LINE} first, free, so you can try it before anything else.",
        "A lot of roofers lose leads just because nobody replies fast enough — I build AI chat that answers instantly and books the estimate. "
        f"I start every conversation with {DEMO_LINE}, no cost, so you can see it work firsthand.",
    ],
}

CTAS = [
    "Mind if I send it over?",
    "No pressure either way — want me to send it your way?",
]


def build_message_variants(primary_service: str, opener: str) -> tuple:
    pitch_1, pitch_2 = PITCHES[primary_service]
    variant_1 = f"{opener} {pitch_1} {CTAS[0]}"
    variant_2 = f"{opener} {pitch_2} {CTAS[1]}"
    return variant_1, variant_2


def build_notes(row: dict, primary_service: str) -> str:
    notes = []
    if not row.get("recent_post_topic", "").strip():
        notes.append("No recent_post_topic — opener fell back to website_status angle; consider a manual once-over.")
    status = (row.get("website_status") or "").strip().lower()
    if status in HAS_SITE_VALUES:
        notes.append(f"Routed to {primary_service} based on follower_count vs. {FOLLOWER_THRESHOLD_FOR_WEB_CHAT}; override if you know better.")
    if row.get("phone_number", "").strip():
        notes.append(f"Phone on file: {row['phone_number'].strip()}")
    return " ".join(notes)


def generate(prospects_path: Path, log_path: Path, output_path: Path):
    new_rows, skipped_rows = filter_new_prospects(prospects_path, log_path)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in new_rows:
            primary_service = route_primary_service(row)
            opener = build_opener(row)
            variant_1, variant_2 = build_message_variants(primary_service, opener)
            writer.writerow({
                "business_name": row.get("business_name", "").strip(),
                "primary_service": primary_service,
                "opener": opener,
                "message_variant_1": variant_1,
                "message_variant_2": variant_2,
                "status": "Not Sent",
                "notes": build_notes(row, primary_service),
            })

    print(f"Wrote {len(new_rows)} prospect(s) to {output_path}")
    print(f"Skipped {len(skipped_rows)} already-contacted prospect(s):")
    for row in skipped_rows:
        print(f"  - {row.get('business_name', '(unknown)')}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prospects", default="outreach/prospects.csv", help="Path to the prospects CSV")
    parser.add_argument("--log", default="outreach/contacted_log.csv", help="Path to contacted_log.csv")
    parser.add_argument("--output", default="outreach/output.csv", help="Path to write the generated batch")
    args = parser.parse_args()

    generate(Path(args.prospects), Path(args.log), Path(args.output))


if __name__ == "__main__":
    main()
