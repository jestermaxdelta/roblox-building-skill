# Team, business and legal basics

The business behind a Roblox game: solo versus team, roles, hiring and commissioning, payment structures and contracts, revenue splits and group payouts, small-team project management, DevEx and tax paperwork, budgeting, IP and licensing, naming and trademarks, selling or acquiring a game, publishers and programmes, sustainable cadence, when to kill a project, and a business health checklist. Open it before the first collaborator touches the place, before any Robux or money changes hands, before using anything you did not make, and whenever a live game's revenue, team or ownership is about to change.

**Not legal, tax or financial advice.** Facts below are dated 2026-11-10 and tagged with their source; platform numbers are `[VS]`. Contract, employment, tax, privacy and IP law differ by country, and anyone under 18 needs a parent or guardian for agreements and payments. Read the current Roblox Terms of Use, Developer Exchange Terms and Community Standards yourself, and pay a qualified professional for contracts, company set-up, tax and any sale, licence or dispute. Tags: `[official]` Roblox docs, `[community]` forum, press or vendor (heuristic), `[VS]` version-sensitive, `[house]` house estimate, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0).

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner (solo or two friends) | (1) Put the game in a group you own, with 2-step verification on the owner account. (2) Write down who owns what and who gets what, even as five lines. (3) Use only assets you made or hold a written licence for; keep a licence log. (4) Know the cash maths: 100 R$ sold ≈ 70 R$ earned ≈ $0.266. (5) If you are under 18, involve a parent or guardian before any deal | Company formation, publishers, trademarks, revenue-share vesting |
| Intermediate (paying people) | Fixed-price briefs with scope, excludes, milestones and ownership on payment; contractors in a sandbox experience on least privilege; group payouts with a written agreement; a monthly budget with a reserve; Publish limited to two leads; a changelog and code review in risk order | Licensed IP, acquisitions |
| Expert (studio) | Team pool with vesting and exit rules; rights audit ready for a brand, licence or sale; blended DevEx rate and withholding in forecasts; brand-deal registration; kill criteria and portfolio planning; quarterly access audit and restore drill | — |

## Contents

1. Solo or team · 2. Roles · 3. The group as the container · 4. Hiring and commissioning · 5. Payment structures · 6. Agreements · 7. Scam patterns · 8. Revenue splits and group payouts · 9. Project management for small teams · 10. Team Create, version control and review · 11. DevEx, tax paperwork and cash flow · 12. Budgeting · 13. IP and copyright · 14. Names and trademarks · 15. Selling or acquiring a game · 16. Publishers, programmes, brand deals and UGC · 17. Burnout and cadence · 18. When to kill a project · 19. Business health checklist · 20. Level-up table · 21. Conflicts · Review gate · Sources

## 1. Solo or team

| Shape | Fits | Costs and risks |
|---|---|---|
| Solo | Small-scope games (the 4-week MVP in `process-and-playtesting.md`), full control, no splits | Every discipline is yours; under house rule 1 that includes Blender art. Bus factor of one; isolation; no reviewer |
| Solo plus contractors | A clear game where bounded pieces are outside your skills (animation set, icon set, music) | Cash now; 20–30% of the contractor's hours come back as your briefing and review time `[lihfolk]` |
| Core team of 2–4 on shares | Ongoing live game needing code, art and design every week | Shares dilute; disputes when someone stops contributing; needs written rules (§8) |
| Studio with payroll | Proven revenue and several games | Fixed costs; hold at least three months of them in reserve before adding another `[lihfolk]` |

Decision rule `[house]`: stay solo until one named bottleneck costs you more weeks than its fixed price would cost in money; hire for that bottleneck only; add a share-holding partner only for a role the game needs every week for the next year.

## 2. Roles

Every hat exists even on a solo project; name who wears each so nothing is ownerless.

| Hat | Owns | Typical first hire? |
|---|---|---|
| Owner / producer | Vision, scope, budget, group ownership, final call | Never outsourced |
| Gameplay programmer | Core loop, data, purchases, security | Core team, not a contractor: this is the game's identity and its risk |
| 3D artist (Blender) | Every visible asset, collision, LODs (`art-pipeline-blender.md`) | Common contractor role; needs the style guide and budgets in numbers |
| UI designer | Screens, tokens, hand-off (`ui-design-figma.md`) | Contractor for a defined screen set |
| Animator, VFX, audio | Feel | Bounded sets; classic fixed-price work |
| Live ops and economy | Update cadence, configs, analytics | Core team once live |
| Community lead, moderators | `community-moderation-safety.md` | Volunteers at first; adults for enforcement powers |
| QA / testers | Device matrix, test universe | Tester role with Playtest only |

Two people must be able to publish, restart servers and flip kill switches; one person doing all of it is the commonest single point of failure `[lihfolk]`.

## 3. The group as the container `[official][VS]`

- A group costs 100 R$ to create. A user-owned game can only give Edit to the owner's friends and pays one person; a group-owned game has roles, per-game permissions, audit logs, a shared balance and payouts, and survives people leaving.
- Own the game **and its assets** with the group from the first publish. Assets belong to whoever uploaded them; a game grant on a restricted asset is permanent and cannot be revoked, and Open Use is irreversible, so decide the uploader before uploading.
- **Owner account:** a dedicated account, unique password, authenticator 2-step verification, backup codes offline; never anyone's daily account, never a shared login `[lihfolk]`. Roblox does not arbitrate internal group conflicts: whoever holds the owner account decides, so write down who holds it and what happens if they leave.
- Group owners are accountable for what happens in the group; a permanently removed group blocks its owner from owning a new one for 90 days.
- Permissions by risk (exact names are in `projects/groups.md`): **critical** = manage roles, assign roles, manage and spend group revenue, delete data stores, manage API keys and secrets (several require 2-step verification to grant); **high** = publish, edit, edit data stores, manage monetisation, moderate experiences (18+ only), ban; **low** = playtest, view analytics, view revenue, view audit logs. Edit and Publish are separate: developers edit, two leads publish.
- Roles can be scoped per game. Give a contractor per-game access on a **separate sandbox experience**, not a second place inside the live universe: permissions attach to the experience, so "just the sandbox place" would open every place in it `[lihfolk]` (follows from per-experience permissions; verify with a test account).
- Place Copying off before any private asset goes in.
- **Age rules for collaboration:** using Team Create with other people requires an age check (ID or facial estimation), and the owner must complete one for collaborators to join. By default only compatible age groups can collaborate; outside them, collaborators must be trusted friends or have a linked parent's permission. A collaborator blocked by the age rules still holds Edit permission: they can Save As a copy to Roblox, use Open Cloud and manage metadata in Creator Hub, so removing access still means removing the role.
- Quarterly access audit, about 20 minutes per game `[lihfolk]`: list everyone with Edit, Publish, secrets, data-store and revenue permissions; read Activity History (publishes, permission and setting changes); remove anyone without a current task; rotate keys and secrets they could see; check Place Copying; record the audit.
- Transferring an existing game into a group: §15.

## 4. Hiring and commissioning

Hire when the work is **bounded**, **outside your skills** and **not the game's identity**; do not hire when you cannot yet write the brief, have no time to review, or have not yet learned whether players want the game `[lihfolk]`.

Where: the DevForum's collaboration and hiring area, Roblox's Talent Hub (referenced by current docs; DevForum threads about it run into mid-2026 `[community: search summary]`), developer Discords, and referrals. r/robloxgamedev regulars push back hard on unpaid and revenue-share-only posts `[community: search summaries of subreddit snapshots]`: expect good people to ignore them.

Portfolio signals `[lihfolk]`:

| Look for | Why |
|---|---|
| Work like yours (low-poly, phone-friendly, your genre) | A realistic showcase says little about a mobile simulator |
| Shipped work in live games | It met real players and exploiters. Ask what broke after release |
| Process: iterations, budgets, before/after | Shows they can hit numbers, not just make one pretty piece |
| Their exact part in team projects | Portfolios overclaim |
| For Blender artists (house rule 1): wireframes, triangle counts, collision meshes, texel density, `.blend` sources | A marketplace kitbash or generated mesh fails the house rules whatever it looks like |

Process:

1. **Paid trial task**, 2–4 hours of real but non-critical work. Unpaid "tests" that look like real work drive good people away and are how scams against freelancers operate `[lihfolk]`. Judge questions asked and time kept as much as output.
2. **Written brief:** task, style references, budgets in numbers (triangles, texture size, instance counts, frame budget), must include, must not include, delivery format, review rule, price, schedule.
3. **First deliverable small and integrated within a week**, so naming, budget and style mismatches show before they repeat across 40 assets.
4. One named owner answers the freelancer within a day; weekly check-in with something to see.
5. Review against the brief. New ideas are new scope and are paid.
6. **Intake check on every delivery** (`networking-and-security.md` §Backdoors): no scripts in art deliveries, no `require(<number>)`, no third-party content without a licence list. Under house rule 1, also confirm it is authored in Blender, not assembled from marketplace models.
7. End well: pay promptly, remove access the same day, credit them if agreed, give honest feedback.

## 5. Payment structures

| Model | Works for | Fails when |
|---|---|---|
| Fixed price per deliverable | Clear, repeatable work: a map, 30 animations, an icon set, one known system | Scope is vague and "small things" keep arriving |
| Hourly or daily with a cap | Bug fixing, consulting, work inside your codebase | No cap, so cost is unpredictable |
| Retainer (N hours a month) | Ongoing live-ops support for an earning game | Nobody ends it when the need ends |
| Percentage (revenue share) | Core team members who will be there in a year | Used for bounded work, or with no vesting and exit rule (§8) |
| Fixed plus a small, time-limited share | Key people accepting below-market pay | The share has no end date |

Rule `[lihfolk]`: pay contractors fixed; give shares only to core team; revenue share is partnership, not pricing, and most games earn little.

Schedules `[lihfolk]`: small jobs 100% upfront from a new client or on delivery for a trusted one; medium 50/50; large by milestone (for example 30% start, 40% first playable, 30% final). Previews (video, a test place the seller controls) before final payment; final files after it.

**Robux or money?**

| | Robux | Money |
|---|---|---|
| Mechanism | Group one-time payout from the group's earned funds (`[official]`: recipient must be a member; 2-step verification challenge) | Bank or payment service |
| Value | 10,000 R$ is $38 at the DevEx rate, and only once the recipient holds 30,000 Earned Robux and passes DevEx review `[official]`. A quote of 10,000 R$ for 20 hours is under $2 an hour `[lihfolk]` | Clear |
| Who carries rate risk | Recipient | Payer, who must DevEx first (4–8 weeks from sale to bank `[lihfolk]`) |
| Trap | "Buy my game pass to pay me": Earned Robux excludes passes sold for template games with no legitimate user visits, direct Robux purchases and Robux transfers `[official]`, so Robux that arrives this way may never be exchangeable | Fees; minors need an adult's account |
| Admin | Low for the payer | Higher; possible reporting duties in your country |

Price evidence is thin and old. One third-party marketplace table (2026) lists scripting at $50–250 for one scoped system, $250–1,000 for a multi-feature module and $1,000–10,000 for saving, monetisation and anti-exploit work; the much-cited DevForum price guide dates from 2021 and warns against using its numbers; one DevForum hirer suggested a 55/15/30 split between scripter, builder and modeller as "a general guideline" `[community: search summaries, single sources]`. Do not treat any of these as a market rate. Derive your own `[lihfolk]`: hourly rate = target yearly income ÷ (hours per week × working weeks × billable share, often 50%); fixed quote = estimated hours × rate × 1.2 risk factor; state the Robux price only after converting through DevEx.

## 6. Agreements (not legal advice)

Most commission disputes are about a scope nobody wrote down `[lihfolk]`. A short written agreement both sides confirm is far better than nothing; anything large, long-running or cross-border deserves a contract reviewed by a professional.

Minimum contents:

1. **Parties:** who pays (person or group, with contact), who works; the approving parent or guardian if either is under 18.
2. **Scope** in testable terms, with an **excludes** list and the testing bar ("tested in Studio with 2 clients").
3. **Price, currency, schedule;** for Robux, the payout method.
4. **Deadlines,** and that they move when the client's inputs are late.
5. **Revisions:** how many, and what counts as one.
6. **Ownership after payment:** assignment (client owns the deliverable) or licence (seller keeps it, client may use it). Carve out the seller's pre-existing modules and tools so they are not signed away by accident.
7. **Asset upload:** who uploads to which account. Cleanest: seller delivers source files (`.blend`, FBX/GLB, PNG, animation files) and the client's group uploads them.
8. **Third-party content:** none without a listed licence.
9. **Portfolio rights and confidentiality:** default "may show after release"; a permanent NDA is priced in.
10. **Cancellation both ways:** client keeps paid milestones' work and pays for work since; seller refunds undelivered work and hands over what exists.
11. **Clean code:** no debug remotes, test cheats or backdoors; a handover note (what it does, config, how to test, known limits).

Team members and co-founders need the same thing plus §8's vesting and exit rules, and a line on who holds the owner account. Verbal agreements are the finding that blocks brand, licence and sale deals later (§13 audit).

## 7. Scam patterns

| Pattern | Who it hits | Defence |
|---|---|---|
| "Do a free test task" that is the real job | Freelancers | Paid trials only |
| "I'll pay after it's in the game" / payment in limited items or "exposure" | Freelancers | Upfront or milestone money; check the Robux actually arrived in transaction history before releasing files `[lihfolk]` |
| Fake payout screenshots; overpayment then refund request | Freelancers | Verify on your own account, never from an image |
| Large percentage of a game that does not exist | Freelancers | Treat shares as speculative; ask for some fixed pay |
| Delivered model with a hidden script or `require` by id | Owners | Intake check; no scripts in art |
| Contractor uploads assets to their own account, later revokes or leaves | Owners | Source files; group uploads |
| "Buy my pass to pay me" Robux that is not Earned Robux | Both | Group payout from earned funds, or money |
| Middleman asking Robux up front to "get a YouTuber" (`growth-and-marketing.md`) | Owners | Deal with the creator's business contact directly |
| "Beta test my game" links, fake staff, cookie theft | Everyone | Never run unknown files or paste scripts; 2-step verification |
| Fake tax or payout emails | Anyone who DevExes | Roblox says tax forms are handled on the Creator Hub Taxes page; never send ID or forms by email reply `[official][lihfolk]` |
| Moving talks to private apps, video calls, requests for personal data | Minors especially | Stay in channels with safety tools; a real client needs none of it |

Contracts do not stop every scam and cross-border enforcement is hard `[community]`: structure the money (small upfront, milestones) so the most either side can lose is one milestone.

## 8. Revenue splits and group payouts

Mechanics `[official][VS]`:

- **One-time payouts:** choose members and amounts, or upload a CSV with `userId` and `payoutInRobux`; 2-step verification challenge and eligibility checks. Some groups do not see Payouts at first (group age, insufficient funds).
- **Recurring payouts:** percentages per game and for the whole group. A game's split pays its members first; the remainder flows into the group split; what is left stays in the group balance. Docs example: a game earns 1,000 R$ with a 40/30/10 game split, so 400/300/100 are paid; the remaining 200 enters a 20/20/10 group split paying 40/40/20; 100 stays in the group.
- Private-server subscriptions keep the percentages in force when the subscription was bought. Games sold through paid access in local currency cannot share payouts across members.
- DevEx is requested by a person, so group revenue reaches a bank only through payouts to members (§11). Group payouts carry the split between standard-rate and 18+-rate Robux through to the recipient `[lihfolk][VS]`.

Maths most teams skip `[lihfolk]`:

- **Shares are of revenue, not profit.** If the owner "keeps 60%" and then pays ads, contractors and assets out of it, the owner can end with 10%.
- **Decide a team pool first** (for example 30–40% of revenue) and allocate from it, or nothing is left for the next key person.
- **Write shares in Robux percentages**, not dollars: the rate has changed before ($0.0035 → $0.0038 in 2025; the 18+ rate in 2026).
- **A member on 5,000 R$ a month waits six months** to reach the 30,000 R$ DevEx minimum. Say so before they start.

Rules to agree before the first payout `[lihfolk]`:

| Rule | Example wording to adapt with a professional |
|---|---|
| Earn-in (vesting) | 0% during a one-month trial, rising to the full share over six months of active work |
| Contribution | "Active" means N hours or named deliverables per month |
| Exit | On stopping, the share continues for 3–6 months (or steps down to a small tail), then ends |
| Removal for cause | Abuse, leaks, sabotage or Roblox-rule breaches end the share at once |
| Sale or transfer | What each holder receives if the game is sold or moved (§15) |
| Rates and currency | Paid in Robux through group payouts at whatever blended rate the recipient realises |

Worked failure `[lihfolk]`: an animator gets 10% "for all animation work", delivers 30 animations and stops; the game earns 50,000 R$ a month; without an exit rule the animator receives 5,000 R$ a month indefinitely while the owner pays someone else for new animations. Bounded work should have been fixed price.

The dashboard percentage is not a contract; it is what moves Robux. The written agreement is what everyone points at when it changes.

## 9. Project management for small teams

Scope gates, milestone exit criteria and the 4-week solo plan are in `process-and-playtesting.md`. Additions:

- **Four layers, four speeds** `[lihfolk]`: vision (one page, rarely changes) → roadmap (3–9 months, Now / Next / Later as outcomes, reviewed monthly) → milestone plan (4–8 weeks, deliverables with exit criteria and owners) → week plan (tasks on a board). Dates belong only to Now. A 200-row task list with dates nine months out is the common failure.
- **Task board:** any tool; columns Backlog → This week → Doing (limit: one or two per person) → Review → Done; every card has an owner and a "done when". Bugs carry severity (crisis table in `community-moderation-safety.md`).
- **Estimates in ranges:** optimistic, likely, pessimistic; expected = (O + 4M + P) ÷ 6. Better still, log estimate versus actual for every deliverable and apply your own multiplier.
- **Capacity, not calendar:** people × days × about 0.65 focus factor. Leave 20–30% of a milestone unassigned as one visible buffer rather than padding each task.
- **The vertical slice is the estimate:** if one zone at final Blender quality took three weeks and the plan has eight zones, the plan says 24 weeks.
- **Change budget:** reserve about 10% of capacity for requests arriving mid-milestone; when it is spent, a new request replaces something of equal size. Keep a scope ledger (date, request, asked by, size, decision, paid for by).
- **Kill list** written at milestone start: what gets cut first, in order.
- **Platform lead-time items** go on the roadmap with owners: maturity questionnaire, asset upload and moderation, products and prices tested in a test universe, odds disclosure and `PolicyService` gates, localisation, thumbnails and video, analytics events before soft launch, phone test pass, the 250 engaged-play evaluation for under-16 reach.
- **Live game capacity split:** roughly 60–70% new content and features, 20–30% fixes and debt, 10% experiments `[lihfolk]`. Without an explicit split, debt gets time only after an incident.
- **Public roadmap:** share themes and items already in the current milestone; never dates for Next or Later.
- A decisions log (date, decision, why, who) and a one-page onboarding note outlive any single member.

## 10. Team Create, version control and review

Tooling (Rojo, Script Sync, Wally, Selene, StyLua, CI) is in `engineering-architecture.md`; Studio mechanics in `studio-workflow.md`. Team rules:

- **Split the trees** `[lihfolk]`: code lives on disk under Git with pull requests; map, lighting and Blender-imported assets live in the place under Team Create; each UI screen picks one home. Packages stay out of synced trees.
- **Live scripting or Drafts is a team decision.** Live scripting is the default and auto-saves every 5 minutes; Drafts mode is off by default, set per experience in File ⟩ Experience Settings `[official]`. One or two scripters: live scripting. Three or more touching the same files weekly: Drafts or Git. Drafts live on one machine: commit at the end of every task and before logging off; a draft older than a day is a warning sign `[lihfolk]`.
- **Etiquette:** claim the area you are working in (a tag or attribute on the folder) and have bulk tools respect claims; announce heavy operations and changes to contracts (remote names, attribute names, module return shapes); one changelog line per task (what, where, how to undo, tested or not); remove test objects; close Studio at the end of the day, because an idle session can save stale state over a revert `[lihfolk]`.
- **Reverting:** only the game owner can revert other editors' changes, and open sessions may auto-save over the revert; disable collaboration or make sure nobody is in the place first `[official]`. Never use Studio undo to roll back shared work; use Script History and Version History.
- **Named save before risky work** and a weekly `.rbxl` export off Roblox; `.blend` sources and an asset-id manifest in the repo; a restore drill once a quarter (place export, Git tag, one test player's data version, a second person publishing) `[lihfolk]`.
- **AI agents in Studio** are collaborators with edit rights: same claims, named saves and review; permissions for Studio MCP are in `networking-and-security.md`.

**Code review** `[lihfolk]`:

- Review for consequences, in risk order: (1) trust boundaries (`OnServerEvent`, `OnServerInvoke`, `ProcessReceipt`), (2) persistence and grants (retries, idempotency, session locks, migrations), (3) yields inside callbacks, (4) lifecycle (connections, threads, per-player instances), (5) types and nil, (6) contracts between client and server, (7) readability last.
- Under about 400 changed lines per pull request; mechanical renames and formatting in their own PR.
- Label comments **blocking / should / question / nit**.
- Formatting, lint and type errors are a tool's job; a PR with failing checks is not reviewed.
- Studio-only teams: walk through Drafts "Compare With Server" with a second person, or review through Script History and the changelog line.
- AI-written code: the author owns every line and answers every question about it.
- Questions that catch what tests miss: what if the client sends −1, NaN or another player's id? Can this grant run twice? What if the player left during this yield?

## 11. DevEx, tax paperwork and cash flow `[official][VS]`

| Item | Value (2026-11-10) |
|---|---|
| Rate | $0.0038 per Earned Robux (30,000 R$ = $114). Balances from before 5 Sep 2025 10:00 PT cash out first at $0.0035. $0.0054 for qualifying spend by age-verified US 18+ players in eligible games (`monetization-and-policy.md`) |
| Minimum | 30,000 Earned Robux; age 13+; verified email; DevEx portal account; W-9 (US) or W-8 (non-US) on file; full compliance with the Terms and Community Standards |
| Frequency | One completed request per calendar month |
| Timing | About 10 business days for a first request after portal registration, about 5 for later ones, plus bank time; no processing on weekends and holidays |
| Portal | Invitation by email after first approval; payment method and tax form within one week or the request is declined and the Robux refunded. Payouts run through Tipalti |
| Name | Legal name only; mismatches delay or disqualify |
| Dashboard | An estimate with up to 24 hours' lag; eligibility is reviewed only on submission |
| Earned Robux excludes | Purchased Robux, subscription grants, item trading or resale, Robux transfers received, gift cards, passes sold for template games with no legitimate visits, moderated content |
| Rejection causes | Unfinished portal registration, missing tax or payment details, too little Earned Robux, Terms violations (scamming, account theft, selling Robux outside DevEx) |

Tax paperwork (Roblox's own page says it does not give tax advice; neither does this file):

- Roblox classifies DevEx payments as **royalties** and collects tax information on the Creator Hub Taxes page; payouts are disbursed through Tipalti, which shows the net amount.
- US persons: Form W-9. With a valid form, no US withholding; without a valid taxpayer number, 24% backup withholding.
- Non-US persons: W-8BEN (individuals) or W-8BEN-E (entities). With valid information, 0–30% US withholding applies to the part of the payout related to sales to US players, depending on residence and any treaty claim; without valid information, 24% backup withholding may apply to the whole payout.
- What you owe at home on the rest is for a tax professional. Habit worth having: set aside a share of every payout until you know the bill, and keep records monthly (earned Robux by source and game, payouts, DevEx date/rate/USD/fees, expenses with receipts, agreements, access list) `[lihfolk]`.

Cash flow `[lihfolk]`: plan four to eight weeks from a sale to the bank (holds, the monthly window, review, transfer). Creator Rewards carry a 60-day hold and passes a 5-day hold (`monetization-and-policy.md`). Reversed purchases remove Robux, so a launch-week spike is not banked until it clears; never promise a contractor money from revenue not yet received. Minors: DevEx is open from 13, but community reports say the payment portal expects an adult to complete set-up; unverified in the docs `[lihfolk][VS]`, so involve a parent before the first big month.

## 12. Budgeting

Unit maths `[official]` rates, `[house]` arithmetic: 100 R$ of list-price sales → 70 R$ earned → $0.266. One dollar of payout needs about 263 Earned Robux, which is about 376 R$ of list-price sales. Regional pricing and Plus discounts change what players pay, so read real receipts, never config prices.

Monthly budget template (example: 500,000 R$ list sales → 350,000 R$ earned → $1,330):

| Line | Share of earned | R$ | USD | Rule |
|---|---|---|---|---|
| Team pool (recurring payouts) | 35% | 122,500 | $465.50 | Fixed by agreement (§8) |
| Ads | 20% | 70,000 | $266 | Only while cost per play stays under the value-per-player ceiling in `growth-and-marketing.md` §3; ad credits bought with Robux are irreversible |
| Contractors and assets | 15% | 52,500 | $199.50 | Fixed-price commitments only; three months of any recurring cost held in reserve |
| Reserve and tax set-aside | 10% | 35,000 | $133 | Untouched until the tax bill is known |
| Owner / reinvestment | 20% | 70,000 | $266 | Flexes with the month |

Rules `[house]`:

- Budget from the **trailing three-month average**, not the best month; revenue swings with updates, events and discovery.
- Commit to nothing fixed that the worst of the last three months could not pay.
- Reinvest or pay out `[lihfolk]`: growing with profitable ads → reinvest heavily; stable and the team needs income → pay out, keep the reserve; declining → reserve for the next project and cut ads that no longer pay; no revenue yet → personal time and reserves only.
- Commission ROI: a $300 commission pays for itself only after about 113,000 R$ of extra list-price sales ($300 ÷ $0.00266 per list R$). Work that cannot plausibly move that much is decoration; it can still be right, but decide it knowingly.
- Robux spent inside Roblox (ads, UGC fees) is worth its DevEx value to you, not its retail price.

## 13. IP and copyright (not legal advice)

Roblox's policy `[official]`: unauthorised use of intellectual property is prohibited and removed, and repeat or egregious infringers lose their accounts. You can infringe even if you did not monetise, credited the creator, downloaded it from the internet, bought a physical copy, saw others use it, or believed it was fair use. Ideas and mechanics are generally not protected; specific expression (code, models, art, music, text, UI art) is `[lihfolk]`.

| Material | Can you use it? | Notes |
|---|---|---|
| Art you modelled in Blender, code you wrote | Yes | Keep `.blend` sources, version history and dates: they are your proof. House rule 1 makes this the normal case and removes most asset-licence risk |
| Contractor work | Only as your agreement says | Ownership on payment, in writing (§6); group uploads |
| Creator Store models, marketplace meshes | **No** under house rule 1, whatever the licence | LihFolk and most guides allow licensed Creator Store assets; this skill does not ship them. Being on the store does not prove an asset is clean either |
| Music and sound | Only with a licence that covers games on Roblox, or audio Roblox itself distributes for in-experience use | "Royalty free" means no per-play fee, not free to use. Community threads in 2026 report both removals of infringing uploads and false positives on original audio `[community]`; keep project files and licences. Boombox or radio features that let players play arbitrary ids import other people's copyright problems (music publishers sued Roblox over this in 2021 `[community: press]`). Roblox's current licensed catalogue was not verified in this pass `[VS]` |
| Fonts | Roblox-provided font families: yes. Outside fonts baked into images: only under a licence allowing it | Text in images also breaks localisation |
| Photos, textures, HDRIs | Per-asset licence; CC0 is the safe class | CC BY needs visible attribution (a credits board); CC BY-NC is unsuitable for a game with paid items; CC BY-SA is hard to satisfy in a game `[lihfolk]` |
| Code libraries | MIT/BSD/Apache: keep the notices in a `Licenses` folder. MPL: share changes to its files. GPL family: many studios avoid it in games. **No licence file means no permission** `[lihfolk]` | Wally does not remove licence duties |
| Real brands, films, anime, sports, artists, celebrities | Not without a licence | Also keep them out of titles, thumbnails and search terms |
| Other games' names, logos, characters, maps, UI art, ripped assets | No | "Inspired by" covers genre and ideas, not layout-for-layout copies. Near-duplicates also lose exposure (`growth-and-marketing.md`) |
| Memes and viral characters | Usually someone's copyright or trademark | Popularity is not permission; ownership of viral characters is often claimed later, when the game is worth suing |
| AI-generated assets | Meshes: no (house rule 1). Text or images: only if the tool's terms allow commercial use and nothing recognisable is reproduced | A copyright notice can be filed against content that copies protected expression "even if it has been modified, including by AI tools" `[official]` |
| Player-made content | You host it | Filter text, give a removal path, expect copied IP in builds |

**Licence log** for every third-party item: asset, source URL, author, licence, date obtained, where used, proof file. It answers a takedown in minutes and is the first thing a brand, licensor or buyer asks for `[lihfolk]`.

**Licensed IP the official way** `[official][VS]`: the Licenses catalogue (Creator Hub ⟩ Explore ⟩ Licenses) lists IP that rights holders offer through License Manager. Licence types: full game, in-game sales (named passes and products in one eligible game) and Marketplace items; perpetual or time-limited; each with a revenue share, content standards, brand guidelines and eligibility set by the rights holder. The game must be public before requesting; you pitch; the holder approves, rejects or conditionally approves. Using the IP early can activate the agreement early. Press coverage describes revenue shares "typically between 10% and 25%", collected automatically, with individual licences outside that range `[community: search summaries]`. Model it like any share: it comes off the top, before the team pool.

**When someone copies you** `[official][lihfolk]`: record evidence (links, dates, your sources and version history); decide whether expression, not just the idea, was copied; file through Rights Manager (after registering as a rights holder and verifying ownership; up to 250 links per request) or send a copyright or trademark notice to Roblox's agent. A notice is a legal statement made under penalty of perjury, and knowingly false notices create liability. Do not retaliate with call-outs or report-brigading: that breaks the Community Standards on your side.

**When someone claims you copied** `[official]`: Roblox notifies you by message and email. Check the licence log. If you have no licence, replace the asset. If the claim is wrong, a counter notice (with your name, address, a statement under penalty of perjury and consent to court jurisdiction) generally restores content within 14 business days unless the claimant sues. Get legal advice before sending one or answering in public.

## 14. Names and trademarks (not legal advice)

- A trademark is a name, logo or design that identifies the source of goods or services `[official]`. A game title can infringe one without copying any art.
- Before investing in a name: search the Roblox catalogue for existing games, groups and UGC with it; search the official trademark databases of the markets you care about (USPTO, EUIPO, WIPO's global search) for games and software; search app stores and social handles. A professional clearance search is cheap next to renaming a live game.
- Pick a distinctive, pronounceable, searchable name; avoid generic genre words alone, another game's name with a suffix, and any brand or character name.
- Renaming a live game breaks search for the old name (`growth-and-marketing.md`); rotate tags, not the base title.
- Registration is territorial and by class of goods; whether and where to register is a question of money at stake. Unregistered use may carry some rights in some countries: ask a professional.
- Own the matching group name, social handles and, for a studio, the domain early.
- Roblox has brand guidelines for its own name and logo; check them before using "Roblox" in a studio name or merchandise `[VS]` (not verified in this pass).

## 15. Selling or acquiring a game (not legal advice)

The market exists `[community: press, search summaries]`: Voldex acquired Brookhaven in February 2025 for an undisclosed sum and earlier a football game in a "multi-million dollar" deal; Bloomberg reporting relayed by Tubefilter described mid-size Roblox companies buying top games "for millions of dollars apiece", including one $3 million offer to an independent creator. Whether and how the Roblox Terms of Use permit selling a game, group or account for real money could not be verified from a primary source in this pass; forum and blog claims conflict. Do not act on any summary, including this one: read the current Terms and use a lawyer.

The platform mechanism `[official][VS]`: **game ownership transfer** moves a game to a group the initiator can publish to.

- Both sides verify email. Private `ModuleScript`s and `InsertService` assets must be uploaded to the receiving group; packages owned by a user may need recreating.
- Requests expire after 7 days; a received game cannot be transferred again for 30 days.
- On acceptance, public access is revoked and all servers close; the new owner sets permissions and releases the game again. Game id, place id and URL are kept.
- Search is unaffected if the title is unchanged and the new owner is in good standing; discovery can be affected for up to 24 hours after re-release.
- Existing private-server subscription revenue goes to the receiving group and ignores revenue splits; new ones follow splits. Card information is removed.
- An Open Cloud API key's effective permissions follow the user who last generated it: regenerate keys after a transfer that changes access.

Due diligence, either side `[house]`, extending the rights audit in `[lihfolk]`:

| Check | Evidence |
|---|---|
| Who really owns the group, game and every asset | Asset list per group and per personal account; ex-members' uploads re-uploaded from source |
| Rights to everything in the game | Licence log; contractor agreements with ownership clauses; no verbal deals outstanding |
| Revenue quality | 12 months of Creator Hub exports: earned Robux by source, payer concentration, share from events, refund reversals |
| Liabilities | Revenue-share promises, licensed-IP terms, subscriptions and season passes already sold and owed, private-server subscriptions |
| Standing | Moderation history, maturity label accuracy, odds disclosure, chat compliance, pending IP claims |
| Operability | Source in Git, `.blend` files, docs, config and secrets inventory, DataStore schema, RTBF templates, who can deploy |
| Player data | Erasure duties transfer with the data |
| People | Minors among owners or contributors; parent or guardian involvement |
| Transition | Who operates during the 30-day lock; earn-out or support period; community announcement |

Players judge a sale by what changes for them: announce it honestly, keep purchased things working, and do not let the new owner's first update be a monetisation push.

## 16. Publishers, programmes, brand deals and UGC

- **Publishers and investors** offer user-acquisition money, live-ops staff, brand relationships and QA in exchange for a revenue share, ownership or exclusivity. Terms are private; the only public data found was one 2021 report of a team keeping all rights while a Roblox-only publisher grew its revenue `[community: single source]`. Questions to settle in writing with a lawyer: who owns the group and the game during and after; share of what (gross Robux, after ads?); term and termination; minimum spend they commit; who controls updates, pricing and monetisation intensity (house rule 3 must survive); what happens to the team pool; reversion if they stop investing.
- **Roblox programmes** `[official][VS]`: Incubator (six-month, milestone-driven, up to 40 experienced teams per cohort; applications closed when read); Jumpstart (for novel games aimed at 18+ players; its FAQ says it is not cash funding or a salary); Brand Link (invite-only brand integrations; a game with 500k+ MAU improves the odds); Brand Developer Directory (at least one game with 4M+ MAU and a 65% like score, submitter 18+). Check status before planning around any of them.
- **Brand deals and your own merchandise are ads** `[official]`: content published for any compensation, or promoting off-platform products, must be registered in Ads Manager ⟩ Ad integrations with invoicing details, labelled clearly as an ad, and submitted for moderation before players see it; violations risk the account's ad eligibility.
- Press reports a Roblox **revenue share on creator brand deals from January 2027**, charged per thousand visits with an ad impression: $1.50 US; $0.75 UK, Canada, Australia, New Zealand, Nordics; $0.20 Western Europe, Japan, South Korea; $0.05 elsewhere; a flat $0.10 after 28 days; registration mandatory since 4 May 2026 `[community: GamesBeat and others, search summaries][VS]`. Price brand work with that fee in the model and confirm the live terms.
- Brand content follows the house rules too: a Blender-built integration in a lobby, never an interruption of play.
- **UGC avatar items as a side line** `[official][VS]`: needs government-ID verification (your own or a linked parent's); 80 R$ upload fee per submission (500 R$ with an emissive mask), generally not refunded on rejection; a refundable publishing advance by item type, repaid from the platform's commission as units sell; base creator commission 30%, plus 40% to the game owner when the item is bought inside a game (you get both in your own game); a higher progressive share applies only to Marketplace purchases priced above the floor; 30-day escrow. Limiteds carry irreversible switches (resale, quantity) `[lihfolk]`. Fan items of someone else's IP are removed; a Marketplace licence from the Licenses catalogue is the legal route. Model the advance as a bet on units sold, author the item in Blender, and never attach gameplay power to an avatar item (house rule 3).

## 17. Burnout and sustainable cadence

Evidence is anecdotal: developers who step back cite the load of constant updates and promotion, and critics describe teams crunching to ship weekly `[community: DevForum and essay, search summaries]`. No measured data on Roblox developer burnout was found.

- `liveops-quests-retention.md` recommends a fixed update day. A fixed day is a promise about **when**, not **how much**: a solo developer can ship a config-only drop (a code, a rotation, a small event) weekly and a real content update every two to four weeks, which matches Roblox's own small-update guidance quoted there.
- Build two updates ahead before promising a cadence; ship from the buffer; refill it in quiet weeks.
- Put events, shop rotations and codes in configs so a "live" week needs no publish and no crunch.
- Capacity split (§9) with real time for debt; a visible milestone buffer; no single person on call every weekend.
- Announce breaks ("no update 22 Dec–5 Jan; double rewards event runs automatically"). Players accept planned silence far better than a missed promise.
- Do not read every comment yourself: a triage rota or a community lead filters (`community-moderation-safety.md`).
- Minors on the team: no deadlines that need skipped school or sleep `[lihfolk]`.
- Warning signs: updates slipping two cycles running, bugs reopened, the owner the only person able to publish, avoiding the feedback channel.

## 18. When to kill a project

Write the kill criteria before building `[lihfolk]`, for example: "after a two-week soft launch and two FTUE iterations, D1 is still under X and value per player is under cost per play." Benchmarks for X are in `audit-existing-game.md`; use your own previous game where you have one.

| Signal | Reading |
|---|---|
| Core loop not fun for 5 minutes after two prototypes | Kill or change the core; polish will not fix it |
| D1 and first-session length do not move after two or three targeted fixes | The promise or the loop is wrong, not the funnel |
| Retention acceptable, monetisation near zero after the default product set | Economy or audience mismatch; one more iteration, then decide |
| Only paid traffic keeps CCU up and value per player stays below cost | Stop ads; if organic does not hold, wind down |
| The team no longer wants to play or work on it | Counts as data |
| A rule or platform change removes the audience (maturity floor, chat dependence) | Redesign or retire |

Sunk cost check: "knowing what we know, would we start this project today?" If not, choose deliberately among: **kill** (take it private, keep data duties), **maintenance mode** (servers up, automated monthly config event, purchases honoured, moderation and erasure duties continue), **reuse** (keep the codebase, Blender kit and tooling for a new game with a real twist, not a clone), or **transfer** (§15). Write a short post-mortem (`process-and-playtesting.md` §9) and tell the community plainly.

## 19. Business health checklist

Run quarterly.

- [ ] Game and all assets are group-owned; owner account dedicated, 2-step verified, backup codes offline; a written succession note.
- [ ] Two people can publish, restart servers and flip kill switches.
- [ ] Access audit done this quarter; Place Copying off; ex-contributors removed; keys and secrets rotated.
- [ ] Every contributor has a written agreement: scope or role, pay or share, ownership, exit. Parents or guardians involved for minors.
- [ ] Share percentages sum to a planned team pool; vesting and exit rules exist; nobody is owed an unwritten promise.
- [ ] Licence log complete; no asset without source file or licence; no brand, meme or other game's content.
- [ ] Monthly records kept: earned Robux by source, payouts, DevEx, expenses, agreements.
- [ ] Budget built on the trailing three-month average; reserve covers three months of fixed costs; tax set-aside untouched.
- [ ] Tax form valid on the Creator Hub; DevEx portal details current; legal name matches.
- [ ] Ads spend is below the measured value-per-player ceiling; no fixed cost depends on the best month.
- [ ] Brand deals and merchandise registered as ad integrations; licensed IP terms modelled.
- [ ] Roadmap has Now / Next / Later; the current milestone has exit criteria, a buffer and a kill list.
- [ ] Code is in Git with reviews; weekly `.rbxl` export; restore drill done this quarter.
- [ ] Kill criteria written for anything in prototype; the last post-mortem's actions have owners and dates.
- [ ] Cadence is one the team has kept for eight weeks without crunch.

## 20. Level-up: symptoms → likely cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| A departed member still owns key assets or the game | User-owned game; personal uploads | Group ownership; re-upload from source; transfer the game (§15) |
| Dispute over "my percentage" | Verbal share; no vesting or exit | Written agreement; team pool; exit rule; mediate early |
| Owner earns little from a game that sells well | Shares of revenue given away before costs | Recompute against the budget table; renegotiate with data; fixed pay for bounded roles |
| Freelancer delivers late or off-style | Vague brief; no early integration | Brief with numbers; first deliverable integrated in week one; milestones |
| Delivered asset breaks house rules or carries a script | No intake check; portfolio not vetted for Blender work | Intake checklist; wireframes and `.blend` in the brief |
| "My fix vanished"; reverted content reappears | Stale drafts; idle sessions; revert with editors present | Drafts protocol; close Studio; disable collaboration before reverting |
| Half-finished build went live | Everyone can publish | Publish for two leads; release checklist |
| DevEx rejected or delayed | Name mismatch; portal not completed in a week; balance at the minimum; non-earned Robux | Legal name; register the day the email arrives; buffer over 30,000; pay people through group payouts |
| Cash crunch after a good month | Spent before funds cleared; budget from the peak | Four-to-eight-week lag in the plan; trailing average; reserve |
| Takedown notice | Unlicensed music, font, image or brand; contractor reused someone's work | Replace; licence log; ownership clauses; counter notice only with advice |
| A deal stalls in due diligence | Verbal agreements, personal-account assets, no licence records | Run the §15 table now, not when the buyer asks |
| Updates slipping, team quiet | Cadence above capacity; no buffer; one person carrying on-call | §17; cut scope, keep the day |
| Project lingers at low numbers for months | No kill criteria; sunk cost | §18 decision with a date |

## 21. Conflicts

- **Creator Store assets.** LihFolk's legal notes treat licensed Creator Store models as usable. House rule 1 forbids shipping them; this file keeps the licence reasoning for code libraries, audio and textures only.
- **Estimate multiplier.** `process-and-playtesting.md` says multiply duration estimates by about 3; LihFolk reports team multipliers of 1.5–2.5 once estimate-versus-actual is logged. Use ×3 until you have ten logged deliverables, then your own number.
- **Revenue-share posts.** Community hiring boards are full of percentage-only offers; r/robloxgamedev regulars and LihFolk both treat them as speculative. House position: fixed pay for bounded work, shares only for core team with vesting.
- **Selling games.** Press reports multi-million acquisitions; forum and blog posts claim sales for real money break the Terms. Neither was verified against the Terms text. Unresolved: check the Terms and a lawyer.
- **Licensed-IP revenue share.** Press gives a typical 10–25% range and also individual examples outside it. Read the licence's own terms in the catalogue.
- **Weekly cadence versus sustainability.** `liveops-quests-retention.md` favours a fixed weekly day; anecdotal reports tie weekly content to crunch. Resolution in §17: keep the day, vary the size.

## Review gate

- [ ] The file's disclaimer was passed on: nothing here was presented to the user as legal, tax or financial advice, and the current Roblox terms plus a professional were recommended for contracts, tax, IP disputes and sales.
- [ ] Group ownership, owner-account security and least-privilege roles are in place before collaborators or contractors get access.
- [ ] Every paid or shared arrangement is written: scope, excludes, price and currency, milestones, ownership, upload account, cancellation, exit.
- [ ] Robux quotes were converted through the DevEx rate and the 30,000 R$ minimum; no payment relies on non-earned Robux.
- [ ] Contractors work in a sandbox experience; deliveries pass the intake check and the house rules (Blender-authored, collision, no marketplace models).
- [ ] Shares come from a defined team pool with vesting and exit rules; the budget table balances on a trailing average.
- [ ] Nothing in the game lacks a source file or a licence-log entry; no real brand, meme, other game's asset or unlicensed music or font.
- [ ] The name was searched in the Roblox catalogue and trademark databases before art and marketing were built on it.
- [ ] Brand content is registered and labelled; licensed IP is used only under an accepted licence.
- [ ] Publish rights are limited; changelog, reviews in risk order, backups and a restore drill exist.
- [ ] Cadence, buffer and kill criteria are written; the quarterly health checklist has a date and an owner.

## Sources

Accessed 2026-11-10.

- `Roblox/creator-docs` at commit of 2026-11-07, https://github.com/Roblox/creator-docs (read): `projects/groups.md`; `projects/group-guidelines.md`; `projects/collaboration.md`; `projects/game-ownership-transfer.md`; `projects/activity-history.md`; `projects/assets/privacy.md`; `projects/update-games.md`; `production/monetization/developer-exchange.md`; `production/monetization/tax-information.md`; `production/creator-store.md`; `production/publishing/ip-guidelines.md`; `production/publishing/rights-manager.md`; `production/publishing/account-verification.md`; `ip-licensing/index.md`; `ip-licensing/creators.md`; `production/promotion/ad-integrations.md`; `creator-programs/incubator.md`, `jumpstart.md`, `managed-brand-integrations.md`, `brand-developer-directory.md`; `marketplace/marketplace-fees-and-commissions.md`
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `28 Business and Careers/` (Hiring Freelancers and Revenue Shares; Commissions Pricing and Contracts; Legal Basics - IP Licenses and Assets; DevEx and Cashing Out; Running a Small Studio as a Business), `50 Team Collaboration and Project Management/` (Team Create Permissions and Workflows; Code Review for Luau Teams; Roadmaps Milestones and Scope Control), `26 Community and Moderation/Groups Roles and Permissions for Studios.md`, `13 Production and Case Studies/Disaster Recovery for a Roblox Game - Places, Code, Assets, Data and Accounts.md`, `37 Avatars and UGC/UGC Pricing Limiteds and Marketplace Rules.md` (read)
- https://devforum.roblox.com/t/what-is-a-fair-price-to-pay-game-builders-and-scripters-in-robux-or-usd/3027798, https://devforum.roblox.com/t/commission-price-guide-for-new-developers/1356888, https://builtbybit.com/forums/roblox-development/ (search summary: price anecdotes; weak evidence)
- https://devforum.roblox.com/t/best-practices-for-collaboration/200437, https://devforum.roblox.com/t/how-to-prevent-scamming-when-taking-offers-from-the-recruitment-category/738931, https://devforum.roblox.com/t/rant-about-public-recruitment-category/388147, r/robloxgamedev "PSA: devs aren't free" via mirror snapshots (search summary)
- https://devforum.roblox.com/tag/talent-hub (search summary: threads through July 2026)
- https://www.pocketgamer.biz/voldex-acquires-hit-roblox-game-brookhaven, https://gamesbeat.com/ugc-company-voldex-acquires-roblox-life-sim-brookhaven/, https://www.tubefilter.com/2025/07/14/indie-game-creators-are-making-millions-selling-their-roblox-worlds/ (search summary), https://www.hcrlaw.com/news-and-insights/buying-or-selling-a-roblox-game/ (search summary only; fetch failed)
- https://devforum.roblox.com/t/introducing-the-licenses-catalog-for-game-changing-ip-partnerships/3816457, https://www.thewrap.com/roblox-opens-ip-license-manager-creators-partners, https://licensinginternational.org/news/gaming-platforms-focus-on-ip-management/ (search summary: licence revenue-share ranges)
- https://gamesbeat.com/roblox-sets-cpm-based-fees-for-creator-brand-deals-starting-in-2027/, https://www.netinfluencer.com/roblox-to-take-cut-of-creator-brand-deal-revenue-starting-2027/ (search summary: 2027 brand-deal fee schedule)
- https://gameworldobserver.com/2021/04/07/gamefam-is-publisher-that-helps-roblox-developers-generate-six-figure-revenues (search summary: publisher anecdote)
- https://devforum.roblox.com/t/farewell-fellow-developers/3392972 and a critical essay on weekly-update crunch at slythergames.com (search summary: burnout anecdotes)
- https://devforum.roblox.com/t/upcoming-music-changes-and-copyright-related-action/130570, https://devforum.roblox.com/tag/copyright, https://www.nmpa.org/ (search summary: music enforcement context)
- `references/process-and-playtesting.md`, `references/growth-and-marketing.md`, `references/monetization-and-policy.md`, `references/engineering-architecture.md`, `references/networking-and-security.md` (read, for consistency)
- Not reachable: reddit.com, devforum.roblox.com, create.roblox.com, en.help.roblox.com (blocked); www.hcrlaw.com and www.tubefilter.com (outside the session's allowed network). The Roblox Terms of Use, Developer Exchange Terms, Community Standards and brand guidelines were **not** read directly; statements about them come from the docs mirror or are marked unverified.
