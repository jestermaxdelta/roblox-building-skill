# Launch checklist: <Title>  — target date <YYYY-MM-DD>

Run top to bottom in the final two weeks. Each line has an owner and a date. Detailed gates are in references/checklists.md; this is the sign-off sheet. (HR) = house rule.

## T-14 days: content and quality freeze

- [ ] Vertical slice to full loop verified; all v1 content in; cut list final. Owner: __ Date: __
- [ ] Five-stranger playtest: fun within 5 minutes; median session ≥ <n> min; no P0/P1 UX issues open.
- [ ] (HR) House-rule scan passes in every place: no visible primitive Parts, every visible mesh collides, invisible helpers have CastShadow off. Walk-through test on every asset class.
- [ ] (HR) Asset manifest complete; duplicate-MeshId audit clean; packages AutoUpdate on; no marketplace or free models.
- [ ] Engineering review gate passed (architecture, security, data, purchases).
- [ ] Performance gate passed on a 2–4 GB Android phone, mid-range phone, tablet, desktop and TV with gamepad; 10–15 minute thermal test; 1-hour server soak.
- [ ] Streaming verified at `StreamingTargetRadius = 64`.

## T-10 days: monetization and compliance

- [ ] Products, passes and (if used) subscriptions created in Creator Hub; ids in the config module; prices displayed via `GetProductInfoAsync`.
- [ ] Receipt handler tested end to end in a published test place, including rejoin after an unacknowledged purchase and two-server replay.
- [ ] Gift flow tested with an offline recipient (MessageAsync delivery).
- [ ] (HR) Offer gate verified: nothing before 10 min and first win; ≥ 8 min gaps; ≤ 3 per session; dismiss suppression; small, dismissible, honest copy.
- [ ] Paid random items: odds UI shows every outcome, sums to 100%, boosted odds live; `PolicyService` fallbacks tested with a restricted test account.
- [ ] No fake discounts, restarting countdowns or false scarcity anywhere in UI or store copy.
- [ ] Rewarded video eligibility confirmed; rewards fixed; placements live.
- [ ] Content-maturity questionnaire submitted truthfully; expected label <Minimal / Mild / Moderate>.
- [ ] All user-generated text filtered on the server.

## T-7 days: discovery and metadata

- [ ] Five custom 16:9 1920×1080 thumbnails (< 3 MB), 2–5 active; icon 512×512 readable at 150 px.
- [ ] Title with status tag and verb phrase; description hook in the first 160 characters; genre set; supported languages set.
- [ ] Video thumbnail (optional): authentic gameplay, no spoken audio or ad text.
- [ ] Share links per channel; invite prompt and referral banner wired and tested.
- [ ] Age-tier plan: launch at <16+ / Select>; under-16 eligibility steps started (verification, 2FA, questionnaire, Plus/Premium or 1,000 R$ fee).
- [ ] Matchmaking weights set (Friends and Occupancy raised for social games).

## T-5 days: analytics and LiveOps

- [ ] Onboarding, Shop, Offer and RV funnels plus economy and custom events verified in the test place dashboards.
- [ ] Every tunable is a Configs key with a correct default; Experiments for the first two tests drafted.
- [ ] Weekly update day chosen and announced; first four updates planned; first event dated with its own currency.
- [ ] Performance Dashboard alerts: crash rate above 2–3%, heartbeat, memory; `ServerLowMemoryWarning` logged.
- [ ] Safety: `BanAsync` tooling, report handling and appeal path ready; ban rules published.
- [ ] Rollback plan: previous version id recorded; data migrations backwards compatible or Migrate To Latest Update chosen.

## T-1 day

- [ ] CI produced the release build; test universe green; production publish approved manually.
- [ ] Private soak with the team for 1 hour on the production place; console clean.
- [ ] Dev and test places are in separate universes; gated sub-places "Secure within universe only".
- [ ] Secrets only in the Secrets store; no keys in scripts or git.

## Launch day (Saturday, inside a seasonal window if possible)

- [ ] Publish at <time>; verify join on phone and PC; watch Performance Dashboard and console errors for the first 2 hours.
- [ ] Monitor PTR, bounce and D1 daily for the first week; fix the largest onboarding funnel drop first.
- [ ] Post the first update on the announced weekly day.

## Sign-off

| Gate | Owner | Date | Result |
|---|---|---|---|
| Design | | | |
| Engineering | | | |
| Compliance (HR) | | | |
| Performance and content (HR) | | | |
| Discovery and LiveOps | | | |
