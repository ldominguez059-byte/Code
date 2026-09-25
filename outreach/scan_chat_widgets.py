#!/usr/bin/env python3
"""Scan each company's website for a chat widget, emails and social links.

Usage:
    python3 scan_chat_widgets.py az_roofing_call_sheet.csv
    python3 scan_chat_widgets.py roofing_contacts_100.csv --out scanned.csv

Reads any CSV with a "Website" column (a bare domain or a full URL), fetches
each homepage plus its /contact page, and writes a copy of the CSV with these
columns filled in:
    Chat Widget      - "NONE" (your best leads) or the widgets detected
    Emails Found     - addresses found on the pages
    Instagram Found  - instagram.com link on the site
    Facebook Found   - facebook.com link on the site
    Scan Status      - ok / error message

Uses only the Python standard library. Run it from your own computer.
"""
import argparse
import csv
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

# Substrings that show a chat / AI receptionist widget is installed.
WIDGETS = {
    "Podium": ["podium.com", "podium-webchat"],
    "Birdeye": ["birdeye.com/embed", "birdeye-widget", "widget.birdeye"],
    "Tidio": ["tidio.co", "tidiochat"],
    "Intercom": ["widget.intercom.io", "intercomsettings"],
    "Drift": ["js.driftt.com", "drift.com/"],
    "LiveChat": ["cdn.livechatinc.com", "livechatinc.com"],
    "tawk.to": ["embed.tawk.to"],
    "HubSpot Chat": ["js.usemessages.com", "hubspot-messages"],
    "Zendesk Chat": ["static.zdassets.com", "zopim"],
    "Olark": ["static.olark.com"],
    "Crisp": ["client.crisp.chat"],
    "Facebook Messenger": ["xfbml.customerchat", "fb-customerchat"],
    "GoHighLevel/LeadConnector": ["leadconnectorhq.com", "msgsndr.com", "widgets.leadconnectorhq"],
    "Smith.ai": ["smith.ai"],
    "Hatch": ["usehatchapp.com", "hatchapp"],
    "Weave": ["getweave.com", "weave-webchat"],
    "NiceJob": ["nicejob.co"],
    "Chatra": ["call.chatra.io"],
    "Jivo": ["code.jivosite.com", "jivosite"],
    "Freshchat": ["wchat.freshchat.com", "freshchat"],
    "Chatbase/AI bot": ["chatbase.co", "botpress", "voiceflow", "landbot"],
    "CallRail Form/Chat": ["callrail.com/companies", "swappy"],
    "ServiceTitan Chat": ["servicetitan.com/webchat", "scheduler.servicetitan"],
    "Housecall Pro": ["housecallpro.com", "online-booking.housecallpro"],
    "Jobber": ["clienthub.getjobber.com"],
    "Signpost": ["signpost.com"],
    "Broadly": ["broadly.com"],
    "Kenect": ["kenect.com"],
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
IG_RE = re.compile(r"https?://(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)/?", re.I)
FB_RE = re.compile(r"https?://(?:www\.)?facebook\.com/([A-Za-z0-9_.\-/?=]+)", re.I)
JUNK_EMAIL = ("example.com", "sentry", "wixpress", "domain.com", ".png", ".jpg",
              ".webp", ".gif", "godaddy", "yourname", "email.com", "@2x")
JUNK_IG = {"p", "reel", "explore", "accounts", "stories", "tv", "sharer"}
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read(2_000_000).decode("utf-8", "ignore")


def normalize(site):
    site = (site or "").strip()
    if not site:
        return ""
    if not site.startswith("http"):
        site = "https://" + site
    return site.split("?")[0].rstrip("/")


def scan(site, timeout):
    base = normalize(site)
    if not base:
        return None
    pages, errors = [], []
    for path in ("", "/contact", "/contact-us"):
        try:
            pages.append(fetch(base + path, timeout))
        except (urllib.error.URLError, OSError, ValueError) as e:
            errors.append(f"{path or '/'}: {getattr(e, 'reason', e)}")
        if len(pages) >= 2:
            break
    if not pages:
        return {"status": "error " + "; ".join(errors)[:120]}
    html = "\n".join(pages)
    low = html.lower()
    found = [name for name, sigs in WIDGETS.items() if any(s in low for s in sigs)]
    emails = sorted({e.lower() for e in EMAIL_RE.findall(html)
                     if not any(j in e.lower() for j in JUNK_EMAIL)})
    igs = sorted({h for h in IG_RE.findall(html) if h.lower() not in JUNK_IG})
    fbs = sorted({h.split("?")[0].rstrip("/") for h in FB_RE.findall(html)
                  if not h.startswith(("sharer", "plugins", "tr", "dialog"))})
    return {
        "widget": ", ".join(found) if found else "NONE",
        "emails": "; ".join(emails[:3]),
        "ig": "; ".join("@" + h for h in igs[:2]),
        "fb": "; ".join("facebook.com/" + h for h in fbs[:2]),
        "status": "ok",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--out", help="output CSV (default: <input>_scanned.csv)")
    ap.add_argument("--timeout", type=float, default=12)
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between sites")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    if "Website" not in fields:
        sys.exit("CSV needs a 'Website' column")

    extra = ["Chat Widget", "Emails Found", "Instagram Found", "Facebook Found", "Scan Status"]
    fields += [c for c in extra if c not in fields]

    no_widget = 0
    for i, row in enumerate(rows, 1):
        site = row.get("Website", "")
        name = row.get("Company") or row.get("Business Name") or site
        if not site.strip():
            row["Scan Status"] = "no website"
            print(f"[{i}/{len(rows)}] {name}: no website")
            continue
        res = scan(site, args.timeout)
        if res.get("status") != "ok":
            row["Scan Status"] = res["status"]
            print(f"[{i}/{len(rows)}] {name}: {res['status']}")
            continue
        row["Chat Widget"] = res["widget"]
        row["Emails Found"] = res["emails"]
        row["Instagram Found"] = res["ig"]
        row["Facebook Found"] = res["fb"]
        row["Scan Status"] = "ok"
        no_widget += res["widget"] == "NONE"
        print(f"[{i}/{len(rows)}] {name}: widget={res['widget']} emails={res['emails'] or '-'}")
        time.sleep(args.delay)

    out = args.out or args.csv.rsplit(".", 1)[0] + "_scanned.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nDone. {no_widget} sites have NO chat widget (best leads). Saved: {out}")


if __name__ == "__main__":
    main()
