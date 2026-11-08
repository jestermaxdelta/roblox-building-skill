# Analytics event plan: <Title>

All events are logged on the server, after the action succeeds, in a published place (a test place first). Limits and API signatures are in references/analytics-and-discovery.md: 120 + 20 × CCU events per minute; 10 funnels × 100 steps; 10 resource types; 20 transaction types; 100 SKUs; 100 custom event names; 3 custom fields; 8,000 field-value combinations. Prefer one event name with fields over many names.

## KPIs and targets

| KPI | Launch target | Source |
|---|---|---|
| PTR | ≥ genre median | Creator Analytics |
| Bounce under 60 s | < <x>% | Creator Analytics |
| D1 / D7 / D30 | <x / y / z>% | Creator Analytics vs similar games |
| Median session | <n> min | Creator Analytics |
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

## Configs keys (tunables)

List every tunable the game reads from `ConfigService` with its code default: offer gate values, boost durations, drop weights, hint delay, starting currency, daily reward amounts, event dates.

## Experiments queue

| Experiment | Variants | Primary metric | Guardrail metric | Duration |
|---|---|---|---|---|
| Offer grace | 10 vs 20 min | ARPDAU | D1 | 14–28 days |
| Hint delay | 5 vs 10 s | FirstUpgrade rate | bounce | 14 days |
| Boost price | 29 vs 49 R$ | revenue per DAU | conversion | 28 days |
| Starting currency | 0 vs 100 | D1 | sink ratio | 14 days |

Under 1,000 DAU statistical power is weak; run fewer, bigger tests.

## Dashboard review cadence

- Daily during launch week: PTR, bounce, D1, crash rate, errors.
- Weekly: funnel drop-offs, economy sink ratio, offer funnel conversion, RV opt-in (target 10–20%+), top SKUs.
- Monthly: D30, LTV, cohort comparison, experiment results.
