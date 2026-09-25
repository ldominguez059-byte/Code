# AI Receptionist Outreach Playbook (Roofing + HVAC)

**Offer:** an AI receptionist and chat widget that answers every call and website chat 24/7, books the inspection or service call, and texts the owner the details. Companies without a website get an AI-built site with both included.

## Files

| File | Use it for |
|---|---|
| `az_roofing_call_sheet.csv` | 117 Arizona roofers sorted by priority. **Start with the "A - best fit" rows.** |
| `roofing_contacts_100.csv` | 100 US roofers |
| `hvac_contacts_100.csv` | 100 US HVAC companies (Instagram DMs) |
| `scan_chat_widgets.py` | Checks which websites already have a chat widget (see below) |

**Priority A:** 10–150 Google reviews. These are small, owner-run shops that miss calls while on jobs, which makes them your best buyers.
**Priority C:** 500+ reviews (these usually already have a call center), sponsored listings, and businesses that aren't roofers. Skip them.

---

## Step 1: Find who has no chat widget (2 minutes)
On your computer, in this folder, run:
```
python3 scan_chat_widgets.py az_roofing_call_sheet.csv
```
It creates `az_roofing_call_sheet_scanned.csv`. Rows where **Chat Widget = NONE** are your hottest leads. The script also pulls any emails and Instagram/Facebook links it finds on each site.

## Step 2: Run the missed-call test (the hook)
Call 10–20 companies **after hours**: weekdays after 6pm, Saturday afternoon or Sunday. For each one, fill in `After-hours test date/time` and `Test result`.
- Voicemail or no answer → use the **Missed-call** scripts below. These convert best.
- A person or answering service picked up → use the **Overflow** scripts.

---

## Instagram DM (Facebook DM works the same way)

**DM 1: missed call (the best opener)**
> Hey {Owner or "team"}! Called {Company} {day} around {time} about a roof question and got voicemail. Totally get it, you're probably on a roof 😅
> Quick thought: most homeowners with a leak just call the next roofer on Google. I set up an AI receptionist that answers every call + website chat 24/7, books the inspection, and texts you the details.
> Want me to build a free demo trained on {Company}? Takes me 10 min, no strings.

**DM 1: overflow (someone answered)**
> Hey {Company}! Love the work on your page 🔥 Quick one: when storm season hits and 20 people call at once, how many go to voicemail?
> I set up AI receptionists for roofers that answer overflow + after-hours calls and website chats, book inspections, and text you the lead. Want a free demo built for {Company}?

**DM 2: when they reply "sure" or "how much"**
> Awesome. Here's a 60-sec demo I made for {Company}: {link or video}. Try calling it or chatting like a customer would.
> Setup takes about a day, and it plugs into your current number and website. Got 10 min this week so I can show you how the leads come through?

**DM 3: no reply after 2–3 days**
> Just floating this back up 👆 Happy to just send the demo video if that's easier.

**DM 4: breakup after 5–7 more days**
> Last one from me! If missed calls aren't a problem for {Company} right now, all good. Mind if I check back before monsoon/storm season?

**Instagram tips**
- Follow the account and like 2–3 posts **before** you DM, or your message lands in "Message Requests."
- **Send a short video (a screen recording of your demo) instead of a link.** Instagram often hides links from accounts that don't follow you.
- Send 20–30 new DMs a day at most per account, and change the wording a little each time.

---

## Email

**Subject:** `Called {Company} last night` / `{Company} missed call` / `quick demo for {Company}`

> Hi {Owner},
>
> I called {Company} on {day} at {time} and it went to voicemail. That's understandable for a busy roofing crew, but most homeowners just call the next company on Google.
>
> I set up AI receptionists for roofing companies. They answer every call and website chat 24/7, book inspections straight onto your calendar, and text you each new lead.
>
> I'd like to build a **free demo trained on {Company}** so you can call it yourself. Want me to send it over?
>
> [Your Name] · [Phone] · [Website]
> [Business mailing address]
> *Not interested? Reply "no" and I won't follow up.*

**Follow-up after 3 days:** "Built a quick demo for {Company} anyway: {link}. Give it a call and see how it handles a leak emergency."

---

## Phone call (during business hours)

> "Hey, is this the owner? This is [Name]. Quick reason for the call: I called you guys last {day} evening and got voicemail, and I work with roofers on exactly that. I set up an AI receptionist that answers every call and chat 24/7 and books the inspection for you. Can I build you a free demo? I just need your email or cell to send it."

**Voicemail:**
> "Hi, this is [Name]. I called after hours the other night and didn't reach anyone, which is what I help roofers fix. I've got a free AI receptionist demo built for {Company}. I'll send it to your Instagram. [Phone]."

---

## Group B: companies with no website
> "I noticed {Company} has {X} five-star Google reviews but no website. When homeowners search '{city} roofer' they can't book you. I build AI websites for roofers with a 24/7 AI receptionist and chat built in, so every visitor or call gets booked. Want a free mockup of yours?"

## HVAC version
Replace "roof/leak/inspection" with "AC/no cool/service call." Your best pitch windows are **the first heat wave (May–June)** and **the first cold snap (Oct–Nov)**, when every HVAC phone rings nonstop.

---

## Staying compliant
- **Calls:** calling a business line to pitch is fine. Don't use robocalls or prerecorded voices.
- **Texts:** don't send cold marketing texts to their numbers (TCPA risk). Text only after they've replied or asked you to.
- **Email:** use your real name and business address, and remove anyone who asks (CAN-SPAM).
