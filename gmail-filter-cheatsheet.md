# Gmail Filters — Auto-Sorting Cheat Sheet

**For:** smhnklvn@gmail.com
**Built from:** your actual mailbox — sender addresses and counts read from the live labels, not guessed
**Purpose:** keep Inbox at zero after the triage, without asking me to re-run it.

> **Revised** after checking the Zoom and IPPIS senders in detail. Two rules below changed because the first draft would have hidden your login codes. Corrections are marked ⟳.

---

## 1. Read this first — how Gmail filters actually behave

1. **Where:** Gmail → ⚙ Settings → **Filters and Blocked Addresses** → **Create a new filter**.
2. **Only new mail is filtered.** Existing mail is untouched. Tick *"Also apply filter to matching conversations"* only *after* you've confirmed a rule behaves — otherwise it retroactively relabels thousands of old messages.
3. **The From box accepts OR lists:** `linkedin.com OR facebookmail.com`. One line, no quotes, no commas, no wildcards. A bare domain matches every address at that domain.
4. **Filters add labels; they don't move or reassign.** If two filters match, the message gets *both* labels. There is no ordering and no priority.
5. **Negation does not work in filter fields.** `-from:foo` works in the search box, not reliably when creating a filter. Narrow the rule instead.
6. **"Skip the Inbox (Archive it)" is the whole trick** — but see §2, because it is also the thing that can bite you.
7. **Tick "Never send it to Spam"** on the bank, lab and school rules. Gmail misfiles BK, Medisell and Cepheid mail, and a rule that skips the inbox will send a real invoice to the archive without you noticing it arrived.

---

## 2. ⟳ The rule that overrides everything: never archive verification codes

**"Skip the Inbox" makes a message invisible.** You only find it if you go looking in the label. For marketing mail that's exactly what you want. For a **one-time login code** it means you can't log in, because by the time you've remembered to check a hidden label the code has expired.

You've since told me you'd rather have full coverage on the money senders than protect eFashe's codes — that's a legitimate call, and A6 reflects it. The rule below still holds for everything else.

Senders in this mailbox that issue codes. **Label them if you like — never tick "Skip the Inbox" on them:**

| Sender | What it sends |
|---|---|
| `ippis-noreply@mifotra.gov.rw` | **IPPIS One-Time verification codes** — every one of these is an OTP, nothing else |
| `no-reply@zoom.us` | Zoom verification codes and password resets, alongside real webinar confirmations |
| `noreply@efashe.com` | Receipts, security alerts **and** one verification code — *you chose to archive this anyway; see A6* |
| `accounts.google.com` | Google security alerts **and** Google sign-in codes |

Also worth knowing: `no-reply@zoom.us` sends password resets and **`Code for signing in to Zoom`**, and `rbc.gov.rw` sends eLearning password resets.

> **Correction:** I previously told you your IPPIS mail was payroll slips. It isn't — I checked, and they're all one-time verification codes. They are also the reason `mifotra.gov.rw` has been **removed** from the HR rule: that rule would have archived your payroll-system codes into a hidden label.

---

## 3. Tier A — the noise (start here)

Each rule: **From:** the text shown → tick **Skip the Inbox** → tick **Apply the label**.

### A1 · `09 Noise/Social` — 3,536 messages (biggest win)
```
linkedin.com OR facebookmail.com OR facebook.com OR twitter.com OR x.com OR instagram.com OR meetup.com OR quora.com OR reddit.com
```
Largest volume, lowest stakes. Create this one first and watch it work.

### A2 · `09 Noise/Promos` — 1,823 messages
```
spotify.com OR canva.com OR envato.com OR adobe.com OR brandcrowd.com OR truecaller.com OR tasklet.ai OR jobseeker.com OR tweet.app OR me.sh OR grammarly.com
```

### A3 · ⟳ `09 Noise/Security alerts` — 1,134 messages
```
accountprotection.microsoft.com OR lastpass.com OR beeper.com OR risa.gov.rw
```
**Do not add `accounts.google.com` and do not add `mifotra.gov.rw`.** Both send login codes. Your existing Google security mail is already filed under this label from the triage — that's fine, it's already done — but new Google codes must keep landing in the inbox.

### A4 · `05 Study/ALX` — 811 messages
```
alxafrica.com OR notification.circle.so OR facesofalxse@substack.com
```
`rwanda@alxafrica.com` was the sender hiding inside your old `A|×` label; this absorbs it permanently.

### A5 · `09 Noise/Product updates` — 694 messages
```
gitlab.com OR neon.tech OR supabase.com OR render.com OR em1.cloudflare.com OR noreply@github.com
```
Use `noreply@github.com`, not `github.com`, so B11 handles `notifications@github.com` separately.

### A6 · ⟳ `04 Money/Mobile Money & Bank` — 626 messages
```
bk.rw OR efashe.com OR airtel.africa OR africa.airtel.com OR mtn.co.rw
```
➕ Tick **Never send it to Spam.**

Your instruction was to point one rule at **all** the money senders — BK, MTN, Airtel, eFashe. That now conflicts with §2: **eFashe sends `Your EFASHE verification code`.** You've chosen coverage, so this rule archives it. The consequence is written down rather than hidden: *if you ever need an eFashe login code, it will not be in your inbox — search `label:"04 Money/Mobile Money & Bank"`.*

Notes on what's actually verified here:
- **BK** — five sender addresses (`onlinebanking@`, `ebanking@`, `bkebanking@`, `ebank@`, `BKcardalert@`), all caught by the bare domain. **Zero OTPs in 626 messages** — I checked, this one is genuinely safe to archive.
- **eFashe** — 9 messages: receipts, security alerts, *and* one verification code.
- **Airtel** — only 2 messages, from **two different domains**: `noreply.airtel.africa` and `africa.airtel.com`. Both are in the rule; one alone would have missed half.
- **MTN** — **zero messages in the entire mailbox.** `mtn.co.rw` is included because you mentioned them, but it is an untested guess. If MTN mail ever arrives from a different domain (e.g. `mtn.rw`), this rule will miss it — and MTN MoMo sends OTPs, so check the sender before assuming.

### A7 · `03 Work/HR & Admin` — 385 messages
```
ubuzima.rw OR rulihospital.rw
```
➕ **Never send it to Spam.** (`mifotra.gov.rw` removed — see §2.)

### A7b · `02 Lab/QC & EQA` — 0 messages today, but you want it ready
```
rbc.gov.rw
```
You're right that this fills up on its own — QC and EQA mail arrives in bursts around testing rounds.

⚠ **Do not tick "Skip the Inbox" on this one.** `rbc.gov.rw` is the Rwanda Biomedical Centre, and your 22 messages from it are your lab's actual correspondence: Cobas C111 calibration failures, Sysmex XQ-320 touchscreen faults, GeneXpert performance evaluations, VTM and TB reagent requests, RSB certificates. It also sends **`Ministry of Health eLearning Platform: Password reset request`**. Archiving that domain would bury the correspondence you most need to act on. **Label only, leave it in the inbox.**

---

## 4. Tier B — work and lab

### B8 · `03 Work/Meetings` — 204 messages
```
zfh.de OR vcrp.de
```
ZFh (Alexandra Gottschalk, Christina Blüm) plus the OpenOlat eLearning server.

### B9 · `02 Lab/Equipment & Suppliers` — 227 messages
```
cepheid.com OR medisellrw.com OR pyramidpharmarw.com OR bsc.rw OR rms.rw
```
Cepheid sends from four addresses (`info@marketing.`, `info@mktg.`, `loise.kariuki@`, `jeandamour.umazimpa@`) — the domain rule covers all four. ➕ **Never send to Spam.**

### B10 · `02 Lab/Samples & Referrals` — 230 messages
```
huzalabs.com
```
The "RBC" product-support stream from `product.support@huzalabs.com`. ➕ **Never send to Spam.**

### B11 · `09 Noise/GitHub bots` — 37 messages
```
notifications@github.com
```
⚠ **Read before ticking.** Your Cloudflare Pages build bots and your *human* PR/review/issue notifications share this exact address. Filters can't see display names, so they cannot be split. If you rely on review requests, **apply the label only and leave "Skip the Inbox" unticked.**

### B12 · ⟳ Zoom — split it, don't choose sides

Zoom is 51 messages and is **not** one undecidable blob. Two of its senders are clean:

**B12a · Zoom's own marketing → `09 Noise/Promos`, archive:**
```
teamzoom@e.zoom.us OR teamzoom@zoom.us OR webinars@e.zoom.us OR noreply-marketplace@zoom.us
```
That's ~35 of the 51 — the promotional bulk.

**B12b · `no-reply@zoom.us` → leave in the inbox. Do not archive.**
It carries three incompatible things: webinar/event confirmations, **login verification codes**, and password resets. Archiving it hides your Zoom codes. This is the one Zoom address with no safe automation.

So the earlier "pick a side" question dissolves: **archive Zoom's marketing, leave its transactional mail alone.** You lose no meeting invites and no codes.

*Worth knowing:* among those confirmations are **Career Talk with Queen Kaze (Jibu HR Manager)** and **Career Talk with Diane Uwamwiza (Zipline recruiter)** — career-relevant, and they stay visible under this split.

### B13 · `05 Study/Admissions` — new label, optional
```
northeastern.edu
```
44 Northeastern Global Admissions emails currently sit under ALX. They aren't ALX. Sibling label or leave as-is — cosmetic.

---

## 5. Tier C — leave these manual

**`02 Lab/NRL Reports` — 131 messages.** A genuine grab bag: your own "Ruli Lab Systems" sends, Microsoft Forms responses, Credly/IBM badge mail, savics.org. No clean sender signature, and the Forms submissions are data you want to notice arriving. Hand-sort.

*Note:* `rbc.gov.rw` (A7b) is closely related — RBC is where NRL correspondence comes from — but I've pointed it at **QC & EQA** rather than NRL Reports because its 22 messages are overwhelmingly equipment faults, calibration failures and reagent requests, not report returns. If you'd rather it fed NRL Reports, move the rule.

**`05 Study/BioMex` — 1 message.** The study looks finished. Retire the label or leave it dormant.

---

## 6. Conflicts — one sender, two homes

| Sender | Ambiguity | Resolution |
|---|---|---|
| `teamzoom@` / `webinars@` / `noreply-marketplace@` | — | Clean marketing → Promos |
| `no-reply@zoom.us` | Codes + confirmations | **Left unsorted in inbox** (§2) |
| `accounts.google.com` | Alerts vs Gemini promos | Kept out of A3 |
| `noreply@efashe.com` | Receipts vs login codes | **You chose coverage** — archived to Money (§2) |
| `notifications@github.com` | Bot builds vs human reviews | Label only, don't archive (B11) |
| `rbc.gov.rw` | Lab correspondence vs eLearning password resets | Label only, don't archive (A7b) |
| `mail@e.adobe.com`, `mail@mail.adobe.com` | Express promos vs subscription receipts | One rule, both → Promos. Acceptable |

---

## 7. The three empty labels — resolved

| Label | Messages | Decision |
|---|---|---|
| `02 Lab/QC & EQA` | 0 | **Kept.** Rule **A7b** (`rbc.gov.rw`), label only, not archived |
| `04 Money/Bills & Airtime` | 0 | **Kept.** Rule **A8** names it as a second label on the money rule |
| `03 Work/Dev & GitHub` | 0 | **Kept.** Rule **A5b** names it as a second label on the GitHub rule |

You said these fill up over time, which is right — and it's a better argument than the one I made. But note the tension: **an empty label plus no rule is what rots; an empty label plus a rule is just a rule that hasn't fired yet.** All three now have rules that fire the moment matching mail arrives, so they're wired up rather than abandoned.

### A8 · attach as a second label on A6
Gmail lets a filter apply multiple labels. On the A6 filter, add **`04 Money/Bills & Airtime`** alongside `04 Money/Mobile Money & Bank`, so nothing money-shaped lands in a single catch-all.

### A5b · attach as a second label on A5
On the A5 filter, add **`03 Work/Dev & GitHub`** alongside `09 Noise/Product updates`, so GitHub and dev traffic stays findable under Work as well as Noise.

---

## 8. Verify — don't assume it worked

1. Create **one** rule (A1). Wait for the next LinkedIn or Facebook mail.
2. Confirm it landed labelled **and** out of the inbox.
3. If it did, create the rest. If not, the From text picked up a stray character — retype it.
4. **Test a code sender too:** trigger a Zoom login while the rules are live. The code must appear in your inbox. For eFashe you've accepted the trade-off — don't test it, just remember the code lives under `04 Money/Mobile Money & Bank` if you need it.
5. After a day, search `in:inbox`. Anything there is either genuine personal mail (the system working) or an uncovered sender (add it).

---

## 9. Monthly, two minutes

- Search `in:inbox`. Any recurring sender is uncatalogued → **edit the existing filter** (Settings → Filters → Edit) and append the domain, rather than creating a new filter. Fewer filters, easier to reason about.
- Before adding any new rule, ask the one question from §2: *does this sender ever send me a code?* If yes, don't archive it.

---

## 10. What this does not do

- **Won't label mail already in your mailbox.** That's done — ~8,900 messages already filed. Filters govern new arrivals only.
- **Won't delete or unsubscribe anything.** Archive only, fully reversible, nothing leaves All Mail.
- **Won't cover senders you haven't received yet.** §9 is the loop that catches them.

Ten filters. That's the difference between an inbox you maintain and one someone maintained for you once.
