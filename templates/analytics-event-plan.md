# Analytics event plan: <Title>

All events are logged on the server, after the action succeeds, in a published place (a test place first). Limits and API signatures are in references/analytics-and-discovery.md §Event API: 120 + 20 × CCU requests per minute; 10 funnels × 100 steps; 10 resource types; 100 custom event names; 3 custom fields. Past 20 transaction types, 100 SKUs or 8,000 combined custom-field values the extra values are grouped as "Other". Prefer one event name with fields over many names. Funnel design and reading: references/tutorial-and-onboarding.md §9.

## KPIs and targets

| KPI | Launch target | Source |
|---|---|---|
| PTR (after 12 Oct 2026 only) | ≥ dashboard benchmark P50 | Acquisition → Home Recommendations |
| Bounce under 60 s, and 61–180 s | ≤ dashboard benchmark P50 | Acquisition → Home Recommendations |
| D1 / D7 / D30 | <x / y / z>%: dashboard P50, or the "Drives triage" rows of the one benchmark table (D1 10.3%, D7 1.6%, D30 0.5%) under 100 DAU | Retention |
| Average session | <n> min (house target 19+) | Engagement |
| Co-play days | | |
| Conversion, ARPPU, ARPDAU | | Monetization dashboard |
| Crash rate | < 2–3% | Performance Dashboard |

## Onboarding funnel (`LogOnboardingFunnelStepEvent`)

| Step | Name | Fires when |
|---|---|---|
| 1 | Spawned | Character loaded and in control |
| 2 | FirstAction | First core verb performed |
| 3 | FirstReward | First currency or item granted |
| 4 | FirstUpgrade | First purchase with soft currency |
| 5 | FirstWin | First completed loop (delivery, round, stage) |
| 6 | SawGoals | Goal ladder or quest UI opened |
| 7 | Session2Start | Second distinct session begins |

## Shop funnel (`LogFunnelStepEvent`, funnelName "Shop", one GUID per open)

| Step | Name | CustomField01 |
|---|---|---|
| 1 | Opened | entry surface (HUD button, prompt, offer) |
| 2 | ViewedItem | item SKU |
| 3 | PromptShown | item SKU |
| 4 | Purchased | item SKU |

## Offer funnel (funnelName "Offer")

| Step | Name | CustomField01 | CustomField02 |
|---|---|---|---|
| 1 | Shown | trigger (after_win, level_up, …) | offer SKU |
| 2 | Viewed | | |
| 3 | Prompted | | |
| 4 | Purchased | | |

Also log a custom event `OfferDismissed` with value = dismiss count.

## Rewarded video funnel (funnelName "RV")

| Step | Name |
|---|---|
| 1 | Offered |
| 2 | Started |
| 3 | Completed |
| 4 | Rewarded |

## Economy events (`LogEconomyEvent`)

| Currency | Flow | Transaction type | Item SKU | When |
|---|---|---|---|---|
| Cash | Source | Gameplay | delivery / quest_<id> / offline | each grant |
| Cash | Sink | Shop | upgrade_<line>_<level> | each soft purchase |
| Cash | Source | TimedReward | daily_<day> | daily reward |
| Gems | Source | IAP | pack_<size> | receipt granted |
| Gems | Sink | ContextualPurchase | boost_<id> | boost bought with gems |
| EventTokens | Source / Sink | Gameplay / Shop | event_<name>_<item> | event |

Always pass `endingBalance`. Keep SKUs under 100 and transaction types under 20.

## Custom events (`LogCustomEvent`)

| Name | Value | CustomField01 | CustomField02 | CustomField03 |
|---|---|---|---|---|
| RoundEnded | duration seconds | result (win/loss) | mode | |
| Rebirth | rebirth count | | | |
| ZoneUnlocked | zone index | | | |
| TradeCompleted | item count | | | |
| ServerLowMemoryWarning | memory MB | | | |
| RemoteGuardViolations | count at threshold | remote name | | |
| FtueBeat | seconds since control | beat name (first_verb, first_reward, …) | | |
| TutorialHint / TutorialSkip | 1 | step id | | |

## Configs keys (tunables)

List every tunable the game reads from `ConfigService` with its code default: offer gate values, boost durations, drop weights, hint delay, starting currency, daily reward amounts, event dates.

## Experiments queue

| Experiment | Variants | Primary metric | Guardrail metric | Duration |
|---|---|---|---|---|
| Offer grace | 10 vs 20 min | ARPDAU | D1 | 14–28 days |
| Hint delay | 5 vs 10 s | FirstUpgrade rate | bounce | 14 days |
| Boost price (sequential change of one product, or Managed Pricing; never duplicate products at two prices) | 29 then 49 R$ | revenue per DAU | conversion | 14 days each side |
| Starting currency | 0 vs 100 | D1 | sink ratio | 14 days |

Each experiment: 14–60 days, up to 2 variants plus control, nothing editable once scheduled; the Custom metric set adds up to 3 metrics built from the events above (for example per-user conversion on onboarding step 5). Write the hypothesis and the sample size first (references/analytics-and-discovery.md §Test design). Under 1,000 DAU power is weak: run fewer, bolder tests or dated before/after cohorts.

## Dashboard review cadence

- Daily during launch week: PTR, bounce, D1, crash rate, errors.
- Weekly: funnel drop-offs, economy sink ratio, offer funnel conversion, RV opt-in rate, top SKUs; the eight-line review in references/analytics-and-discovery.md.
- Monthly: D30, LTV, cohort comparison, experiment results.
