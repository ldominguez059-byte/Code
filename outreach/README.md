# Cabren Outreach Prep

Local, offline tooling that turns a CSV of roofing prospects into personalized
IG/FB DM copy for you to send yourself. **It does not log into, browse, or
automate anything on Instagram or Facebook** — it only reads/writes CSV files
and generates text.

## Files

- `prospects.csv` — your input. Replace the sample rows with real ones. Required columns:
  `business_name, city/state, instagram_handle, facebook_page_url, follower_count, recent_post_topic, website_status, phone_number`
  (`website_status` should be one of: `has site`, `no site`, `outdated`)
- `contacted_log.csv` — the log you maintain of who's already been messaged.
  Add a row any time you send a first DM (business_name is enough to match, but
  filling in instagram_handle/facebook_page_url too makes matching more reliable).
- `dedupe.py` — standalone script/module that filters `prospects.csv` against
  `contacted_log.csv`. Matches on business_name, instagram_handle, or
  facebook_page_url (normalized, case-insensitive) — a hit on any one counts as
  "already contacted."
- `generate_messages.py` — the main script. Dedupes, routes each prospect to a
  primary service, and writes `output.csv`.

## Usage

```bash
# check who'd be skipped as already-contacted, without generating anything
python3 outreach/dedupe.py outreach/prospects.csv outreach/contacted_log.csv

# generate the batch
python3 outreach/generate_messages.py
# or with custom paths:
python3 outreach/generate_messages.py --prospects outreach/prospects.csv --log outreach/contacted_log.csv --output outreach/output.csv
```

`output.csv` columns: `business_name, primary_service, opener, message_variant_1,
message_variant_2, status, notes`. Open it in Excel/Sheets, copy a variant into
Instagram/Facebook DMs yourself, then update the `status` column
(`Not Sent` / `Sent` / `Replied` / `Booked` / `Not Interested`) as you go — and
add a row to `contacted_log.csv` once you've sent it, so it's never regenerated.

## Routing logic (default — no extra ICP filters given)

- `website_status = no site` or `outdated` → **Website Build**
- `website_status = has site`, `follower_count >= 1000` → **AI Web Chat**
  (already active on social, likely fine with a chat-first flow)
- `website_status = has site`, `follower_count < 1000` → **AI Receptionist**
  (missed-call is the more universal pain point for a smaller/less-online crew)

This is a starting assumption, not a hard rule — tune the threshold or logic in
`generate_messages.py` (`route_primary_service`) if you find better signal
(e.g. crew size, service area, or notes you want to feed in per-row).

## Tone

Both variants are written in a friendly-local-peer voice — casual, no jargon,
soft CTA ("mind if I send it over?"), always leads with the free demo before
any mention of a retainer. Variant 1 and variant 2 use genuinely different
pitch phrasing (not just a reworded CTA) so replies actually tell you
something about which angle lands.

## Notes on personalization

The opener prioritizes `recent_post_topic` when present; otherwise it falls
back to a website-status-specific angle (no site / outdated). Rows missing
`recent_post_topic` get flagged in the `notes` column as worth a manual
once-over before sending.
