---
name: credit-repair-toolkit
description: |
  Run a full DIY credit-repair pass for a person: extract negative tradelines from Equifax/Experian/TransUnion reports, cross-reference accounts across bureaus, draft FDCPA/FCRA/goodwill/MOV letters, and set up a 30-day dispute-escalation tracker. Trigger on "check my credit report", "dispute this collection", "help me fix my credit", "cross-check my bureau reports", or when the person uploads credit report PDFs and asks what's wrong / what to do about it. Works for the user's own credit or, with the Scope Check in Step 0, for someone they're helping.
---

# Credit Repair Toolkit

A repeatable pipeline: **extract → cross-reference → draft → track → escalate**.
Built from a real dispute campaign (5 collection accounts, 3 bureaus) — generalized
so it works for anyone's report, not just the original case.

---

## Step 0 — Scope check (always do this first)

Before touching any report, confirm:

1. **Whose credit is this?** If it's not the person you're talking to, flag —
   gently, once — that drafting FDCPA/FCRA letters *for* someone else can
   brush up against unauthorized-practice-of-law territory depending on the
   state and how far it goes. Templates and education are fine; acting as
   someone's representative, signing on their behalf, or negotiating directly
   with creditors *as* them is not something this skill should do. Ask
   whether they want templates the other person fills in themselves, or
   whether they're formally authorized (power of attorney, etc.) to act for
   them. Don't block the task over this — just make sure it's the person's
   informed choice, then proceed.
2. **What data do you actually have?** Don't proceed past Step 1 without at
   least one bureau report. If the person describes accounts from memory
   ("I think I have a collection from Midland"), say so explicitly rather
   than treating recollection as report data — recollection can be wrong on
   amounts, account numbers, and creditor names, all of which matter for a
   dispute letter.
3. **No fabrication, ever.** Every account number, balance, date, and
   creditor name in a letter must trace back to an actual report. If a
   report is missing (e.g. only 2 of 3 bureaus provided), say so plainly
   rather than inferring the third bureau's data from the other two.

---

## Step 1 — Extract negative tradelines from each report

Reports typically arrive as PDFs (Equifax, Experian, TransUnion, or a
tri-merge report from a monitoring service). Use `pdfplumber` for text
extraction — reports are dense and multi-column; don't try to eyeball them
from a rendered image.

```python
import pdfplumber
with pdfplumber.open('report.pdf') as pdf:
    text = ''.join((p.extract_text() or '') + '\n' for p in pdf.pages)
```

For each account, pull:
- **Account name / furnisher** (e.g. "Jefferson Capital Systems")
- **Account number** (usually masked to last 4 — that's fine, still a unique key)
- **Original creditor** (if the account was sold — critical for chain-of-title disputes)
- **Balance** (and note if the report's own status line and balance-history
  table disagree — that internal inconsistency is itself dispute ammunition)
- **Date opened / date of first delinquency**
- **Status** (collection, charge-off, current, paid, etc.)
- **Pay status / remarks** (bureaus often bracket adverse info, e.g. `>Collection<`)

Only extract items that are genuinely negative: collections, charge-offs,
repossessions, judgments, late-payment histories on otherwise-open accounts.
Skip satisfactory/current accounts — they're not dispute candidates.

Grep is often faster than a full parse for locating a known creditor name
across a 100+ page report:
```bash
grep -n -i "JEFFERSON\|MIDLAND\|PORTFOLIO RECOVERY\|LVNV" report.txt
```

---

## Step 2 — Cross-reference across bureaus

Build one row per unique account (keyed by furnisher + original creditor +
approximate open date, since account numbers are masked differently by each
bureau) and compare:

| Check | What it tells you |
|---|---|
| Present on all bureaus? | If missing from one, that's not necessarily an error — bureaus don't always receive the same furnisher data. Flag it, don't assume it's already resolved. |
| Balances match? | Mismatches are dispute-worthy on their own. Also check *within* one bureau's own report — status-line balance vs. balance-history-table balance sometimes disagree (real example: Experian showed $386 in one place and $486 in another for the same account). |
| Same original creditor across bureaus? | If two accounts from the same collector have *different* original creditors, they're genuinely separate debts, not a duplicate — don't flag as a duplicate-debt dispute if the original creditors differ. If they *match*, investigate for double-reporting of the same debt (a real dispute angle). |
| Dates consistent? | An account opened/reported at wildly different dates across bureaus is worth a specific "why does this differ" line in the dispute. |
| Statute of limitations | Note the state's SOL for the debt type if known, but don't advise on this beyond flagging it — SOL calculations get jurisdiction- and debt-type-specific fast; suggest the person verify with a consumer-law resource or attorney for anything time-barred. |

Present the cross-reference as a table, not a wall of prose — the person
needs to scan it and confirm before letters go out.

---

## Step 3 — Draft letters

Four letter types, each for a different actor and a different legal basis.
**Never send more than one dispute per letter to the same account+bureau
pair covering different rounds simultaneously** — that muddies the 30-day
clock.

### FDCPA Debt Validation (to the collector, not the bureau)
Use when a debt buyer (LVNV, Midland, Portfolio Recovery, Jefferson Capital,
etc.) is collecting. Demands proof of: amount owed, chain of ownership from
original creditor, and their legal right to collect. Collector must cease
collection activity until validated.

### FCRA Bureau Dispute (to Equifax/Experian/TransUnion)
Disputes the *tradeline as reported*, separate from the collector itself.
Bureau has 30 days (15 U.S.C. § 1681i) to investigate or delete. Include:
identifying info for file match (name, DOB, last-4 SSN, current address),
a table of disputed accounts with account numbers and specific reasons
(not just "this isn't mine" — specificity gets better results), and a
request for the furnisher-contact details used in their investigation.

### Method of Verification (MOV) follow-up
Use only *after* a bureau responds "verified" to round 1. Demands specifics:
which furnisher was contacted, what documents were reviewed, the name of
the furnisher's compliance contact. Many debt buyers can't produce this for
old, resold debt — that's the point of asking.

### Goodwill Deletion
Different track entirely — for **paid, closed** accounts with an otherwise
clean history where you're asking the *original creditor* (not a collector)
for a courtesy deletion, not disputing accuracy. Tone is different: polite
request, not a legal demand. Doesn't work on unpaid collections.

**Template structure for all four:**
```
[Sender info] -> [Recipient] -> [Re: subject line with legal citation if applicable]
-> [Identifying info block, if bureau-facing] -> [Body: what's disputed + why,
specific not generic] -> [Numbered list of what you're requesting] ->
[Closing + signature line] -> [Enclosures note]
```

Always leave `[bracketed placeholders]` for the person's own identifying
info (name, address, SSN last-4, DOB) — never fabricate or guess these,
even if a prior report shows old addresses on file. Multiple historical
addresses on a report are normal; only the person knows their *current*
one.

Save letters as a single Markdown file per batch (e.g.
`FCRA_Dispute_Letters_<Bureau1>_<Bureau2>.md`), grouped by recipient, with
a short notes section at the end covering: how to send (certified mail vs.
online portal — either is valid, certified just gives a hard delivery date),
what happens next per letter type, and any account-specific leverage points
found during cross-referencing (like the balance-inconsistency example).

---

## Step 4 — Set up the dispute tracker

If the person has an existing Notion/database system, extend it rather than
building a parallel one — check for something like a "Collections" or
"Disputes" database first. If extending an existing DB, add (don't
replace) these fields:

| Field | Type | Purpose |
|---|---|---|
| Dispute Sent Date | Date | When the letter actually went out (not when drafted — these differ) |
| Response Due (30d) | Date | Sent date + 30 calendar days |
| Escalation Stage | Select | Letter Sent -> Verified-Send MOV -> No Response-File CFPB -> AG Complaint Filed -> Resolved/Deleted |

If there's no existing system, a flat table (spreadsheet or a simple Notion
database) with those three fields plus Account/Balance/Bureau-or-Collector
is enough to start.

**Important distinction when populating dates:** if a letter was mailed
today, that's a real Dispute Sent Date. If a letter was *drafted* today but
still has unfilled bracketed placeholders waiting on the person, the clock
hasn't started — say so explicitly rather than back-dating the tracker to
look further along than it is.

---

## Step 5 — Escalation ladder (what Escalation Stage actually means)

| Stage | Trigger | Next action |
|---|---|---|
| Letter Sent | Letter mailed/submitted | Wait for response or the 30-day deadline |
| Verified - Send MOV | Bureau/collector responds "verified" without real detail | Draft and send MOV request |
| No Response - File CFPB | 30-day deadline passes with no response | File at consumerfinance.gov/complaint — free, logged publicly, 15-day forced response |
| AG Complaint Filed | CFPB complaint also stalls, or violation is clear-cut | State Attorney General's consumer protection division |
| Resolved/Deleted | Item removed or corrected | Done — update Balance/Deleted fields, archive the row |

Small claims court (FDCPA/FCRA statutory damages, up to $1,000/violation
plus actual damages) is the sharpest tool available but sits outside this
skill's automation — flag it as an option when a collector clearly ignored
validation or a bureau blew its deadline, don't draft court filings here.

---

## Edge cases

- **Report only partially machine-readable** (scanned/image PDF): fall back
  to page rasterization + visual read per the pdf-reading skill rather than
  guessing from a failed text extraction.
- **Same debt, different collectors on different bureaus** (debt resold
  mid-dispute): flag this explicitly — it changes which FDCPA letter target
  is current, and an old collector's letter may now be moot.
- **Judgment accounts**: handle separately from standard collections — a
  judgment has already been through a court, so the playbook is Vacate /
  Satisfaction of Judgment negotiation with the creditor's attorney, not a
  standard FDCPA validation letter. Don't send a validation letter to an
  attorney enforcing a judgment as if it were a standard debt-buyer account.
- **Uncertain whether two tradelines are the same debt**: don't guess.
  State what would confirm it (e.g. "an attorney payoff letter would confirm
  this is the same account") and track it as an open question, not a
  resolved fact, until confirmed.

## Cadence

Not a scheduled/recurring skill — triggered per dispute round. A natural
follow-up cadence is checking the tracker around each Response Due date and
advancing Escalation Stage accordingly; that check can be scheduled if the
person wants a recurring reminder.
