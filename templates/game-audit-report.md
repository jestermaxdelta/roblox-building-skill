# Game audit report: <Title>

Fill top to bottom while running `references/audit-existing-game.md`. Every score needs an evidence line (number, screenshot name, script path and line, or timed observation). Delete nothing; write "no data" where there is none. `[VS]` facts used: re-check at create.roblox.com/docs before acting.

| Field | Value |
|---|---|
| Universe ID / place ID(s) | |
| Audit date / auditor | |
| Live place version at audit | |
| Genre / age guideline / Kids-Select status | |
| Public since / last update / fixed update day | |
| Source of truth (Rojo repo, Script Sync, Studio) | |
| Data layer and schema version | |
| Access used (dashboard screenshots, Open Cloud analytics, Studio MCP, repo) | |
| 6-week goal and target metric | |
| Developer level (beginner / intermediate / expert) and how it was set | |

Report shape by level: **beginner** fill sections 0, 2 (scores only), 3 and the safe-change checklist, and write section 0 in plain language; **intermediate** fill everything except the expert rows; **expert** fill everything, including evidence grades, dismissed findings, experiment plans and the second-opinion block.

## 0. Top 3 actions, explained (always fill; this is the whole plan for a beginner)

Blockers first. For each action: what to change, why it matters to a player, exact steps, how to tell it worked and when.

| # | Action | Why (one sentence a new developer understands) | Steps | Worked if (number and date) | Reference to open |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## 1. Numbers (baseline window: <YYYY-MM-DD> to <YYYY-MM-DD>)

Benchmark = the game's own Creator Analytics benchmark (state the type: similar players / genre / all). If under 100 DAU, write the fallback source from the audit reference §2.

| Metric | Game | Benchmark P50 | Benchmark P90 (or P10) | Trend vs 30 days ago | Source |
|---|---|---|---|---|---|
| DAU / peak CCU | | n/a | n/a | | |
| Home Recommendations impressions per day | | n/a | n/a | | |
| Play-through rate (after 12 Oct 2026 only) | | | | | |
| First-play bounce < 60 s | | | | | |
| First-play bounce 61–180 s | | | | | |
| Still playing at 5 min (first-session curve) | | n/a | n/a | | |
| D1 / D7 / D30 retention | | | | | |
| Play days per user D2–7 / D8–28 | | | | | |
| Average session time | | | | | |
| Playtime per user per day | | n/a | n/a | | |
| Intentional co-play days | | | | | |
| Payer conversion | | | | | |
| ARPPU / ARPDAU | | | | | |
| Like ratio / comments read | | n/a | n/a | | |
| Client crash rate / out-of-memory exits (worst platform) | | n/a | n/a | | |
| Client FPS, low-end Android | | n/a | n/a | | |
| Client memory usage % (worst platform) | | n/a | n/a | | |
| Server frame rate / server memory | | n/a | n/a | | |
| Join-to-playable (timed, low-end phone) | | n/a | n/a | | |

Acquisition mix (share of new users): Home recommendations __% · Search __% · Friends __% · Sponsored __% · Share links / other __%.

Things that changed in the baseline window (updates, thumbnails, title, ads, prices, platform events):

- 

## 2. Scorecard (0–5 each; no numbers → max 3; house-rule, policy, data-loss or client-trust hit → max 1)

| # | Dimension | Score | Evidence (one line, with source) | Biggest gap |
|---|---|---|---|---|
| 1 | First session (FTUE) | | | |
| 2 | Core loop | | | |
| 3 | Progression and economy | | | |
| 4 | Retention and LiveOps | | | |
| 5 | Monetisation | | | |
| 6 | UI/UX | | | |
| 7 | Art, cohesion, house rules | | | |
| 8 | Performance | | | |
| 9 | Security and data | | | |
| 10 | Discovery and growth | | | |
| | **Total / 50** | | | |

Sub-checks (pass count out of 6; under 3 caps the parent at 2, 3–4 caps it at 4; a blocker item goes to section 3):

| Sub-check | Parent | Passes / 6 | Failed items | Cap applied |
|---|---|---|---|---|
| 2a Game feel and audio | Core loop | | | |
| 6a Accessibility and quality of life | UI/UX | | | |
| 4a Community and safety | Retention and LiveOps | | | |

Timed first-session log (from the MCP play pass or a recording):

| Moment | Seconds from join | Note |
|---|---|---|
| Playable (control of character) | | |
| First reward | | |
| First upgrade or purchase with soft currency | | |
| Goal ladder first visible | | |
| First prompt of any kind (offer, group, notification, invite) | | |
| First Robux offer | | |
| First moment worth a clip | | |

House-rule scan result (paste the output or "House-rule scan OK"):

```
```

Census highlights (instances, scripts by container, remotes, unique MeshIds, flags):

- 

## 3. Diagnosis

- Triage step reached (T0–T8): __ because: __
- Blockers (T0), if any: __
- Platform causes ruled in or out (seasonality, competitor, algorithm change, 12 Oct 2026 measurement change): __
- What is working and must not be broken: __

## 4. Findings and ranked actions

Priority = Impact (1–5) × Confidence (0.2 / 0.4 / 0.7 / 1.0) ÷ Effort (dev-days, min 0.5). Blockers and house-rule violations are listed first regardless of score. In the Evidence column start with the grade: Measured, Observed, Static (not measured) or Inferred. Code findings add P0–P3.

| Rank | Action | Dimension | Evidence | Metric it should move | I | C | E | Priority | Flag or experiment | Reference to open |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |
| 6 | | | | | | | | | | |
| 7 | | | | | | | | | | |
| 8 | | | | | | | | | | |
| 9 | | | | | | | | | | |
| 10 | | | | | | | | | | |

Parked (real but below the line), one line each:

- 

Dismissed findings (pattern or suspicion, location, why it is not a problem), so the next audit skips them:

- 

Stopwatch comparison (optional; use when there is no dashboard benchmark). Fresh account, phone:

| Measure | Leader A | Leader B | Peer C | This game |
|---|---|---|---|---|
| Load to control (s) | | | | |
| First action (s) | | | | |
| First reward (s) | | | | |
| Pop-ups in first 3 min | | | | |
| First purchase prompt (min) | | | | |

## 5. Decision

- [ ] Quick-wins sprint · [ ] Rebuild the loop in the same universe · [ ] Park or kill
- Rule that triggered it: __
- Lower-risk option: __ · Bolder option: __ · Recommended: __

Second opinion (required for rebuild, park, save-schema migration, live pricing or a ship decision; optional otherwise):

| Field | Value |
|---|---|
| Question as framed (neutral wording) | |
| Rubric fixed before answers (3–5 points) | |
| Evidence pack given to every reviewer | |
| Tier and reviewers (quick: 1 sceptic; standard: player advocate, systems engineer, producer or sceptic) | |
| Reviewer verdicts and confidence | |
| Strongest objection, and whether it changed the recommendation | |
| Evidence that would flip the decision | |

## 6. Two-week plan (quick wins)

One target metric. One variable per dimension per week.

| Day | Change | Config key or experiment | Owner | Measured by | Rollback trigger |
|---|---|---|---|---|---|
| 1–2 | Instrument what is missing (funnels, economy events); baseline locked | | | | |
| 3–5 | | | | | |
| 6–7 | Release 1; watch 2 h; announce | | | | |
| 8–12 | | | | | |
| 13–14 | Release 2; re-read numbers; decide next step | | | | |

Expected result (state the number and the date it can first be read): __

## 7. Six-week plan

| Week | Theme (one dimension) | Deliverable | Target metric and value | Gate to pass |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | Re-audit: rescore all ten dimensions | New report | Total / 50 vs today | Gate A |

Weekly update day: __ · Events planned: __ · Growth actions unlocked when (metric ≥ value): __

## 8. Safe-change checklist for this plan

- [ ] Baseline metrics and live place version recorded above.
- [ ] Version History note added; local `.rbxl` and git tag saved.
- [ ] Test universe used for all writes; no production DataStore access from Studio or MCP.
- [ ] Every behaviour change behind a Configs key whose default is the old behaviour.
- [ ] Experiment or cohort comparison chosen for each change; guardrail metrics named.
- [ ] Save schema: additive only, version bumped, migration tested on copies of real profiles, old servers can still read it (or outdated servers restarted immediately).
- [ ] Nothing a player paid for is removed or weakened; compensation planned where a paid item changes.
- [ ] Release at off-peak; restart only outdated servers with a delay; in-game countdown wired.
- [ ] Alerts set (crash rate, out-of-memory exits, server frame rate); Performance dashboard watched by place version for 2 h.
- [ ] Rollback triggers written; rollback path = flip Config, then restore version, publish, restart.
- [ ] Update announcement, event and in-game changelog drafted.

## 9. Open questions and unchecked facts

| Item | Who answers | Needed by |
|---|---|---|
| | | |

## 10. Re-audit log

| Date | Total / 50 | Target metric | Changes shipped since last audit | Kept / reverted |
|---|---|---|---|---|
| | | | | |

Deliverable scores (0–10; any failed gate caps at 5.0; 8.5 or more to call it done; at most three fix rounds):

| Date | Deliverable | Gates | First score | Final score | Rounds | Lowest criterion and the fix that moved it |
|---|---|---|---|---|---|---|
| | | | | | | |
