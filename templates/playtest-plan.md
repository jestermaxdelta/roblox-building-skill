# Playtest plan: <Title> — build <version> — <date>

Method notes and interpretation rules are in references/process-and-playtesting.md §7; the timing targets below are the house targets from references/tutorial-and-onboarding.md §1–2, and a recording of each phone session is what its §13 rubric is scored from. The default session is five strangers, observed silently, with a short interview afterwards. Run one every week from the first playable prototype.

## Goal of this test

- **Question we must answer:** <one sentence, e.g. "Do new players find the upgrade shop within the first 3 minutes without prompting?">
- **Hypothesis:** <what we expect and the number that would confirm it>
- **Kill / keep criterion (prototype stage):** <e.g. at least 3 of 5 replay voluntarily; median session ≥ 6 min>

## Build and setup

- Place and version: <> (a private test place, never production).
- Device mix: at least two phones (one 2–4 GB Android), one PC, one gamepad if the game supports it.
- Analytics: onboarding funnel enabled in the test place; `debug.profilebegin` labels on hot loops; console capture on.
- Reset test accounts to fresh profiles (`ProfileStore.Mock` or a wiped test key).
- Recording: screen capture with consent; timestamped observer notes.

## Participants

| # | Persona (new / returning / target age tier / platform) | Recruited from | Device |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

## Session script (45 minutes)

1. 0–5 min: consent, "think aloud if you like", no instructions about the game.
2. 5–30 min: free play. Observers do not help. Note the time of each milestone below.
3. 30–40 min: interview (questions below).
4. 40–45 min: thanks; ask whether they would play again tomorrow and why.

## Milestone timing sheet (per participant)

| Milestone | Target | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|---|
| In control (from join, on the 2–4 GB phone) | ≤ 10 s (15 s ceiling) | | | | | |
| First action (from control) | ≤ 15 s | | | | | |
| First reward (from control) | ≤ 30 s | | | | | |
| First upgrade | < 2 min | | | | | |
| Found the shop unprompted | < 3 min | | | | | |
| First win / loop complete | < 5 min | | | | | |
| Saw the goal ladder | < 5 min | | | | | |
| First "I want to…" statement | | | | | | |
| Confusion events (count) | 0–2 | | | | | |
| Quit or idle moments | 0 | | | | | |
| Frame hitches noticed | 0 | | | | | |

## Observation prompts

- Where did they look first? What did they try that did nothing?
- Which UI element did they not see? Which did they tap by mistake?
- When did they smile, laugh or lean in? When did they sigh?
- Did they read any text? Which?
- On touch: which buttons were hard to reach? Did they hit the reserved zones?

## Interview questions (ask, then listen)

1. Describe what you were doing, in your own words.
2. What were you trying to achieve at the end?
3. What was the most fun moment? The most annoying?
4. What did you want to buy or unlock, if anything? Did anything feel like a nag?
5. Would you play again tomorrow? What would bring you back?
6. What would you tell a friend this game is about?

Do not ask "did you like it?" and do not explain the game before they answer.

## Interpretation rules

- Trust behaviour over opinion; trust timings over adjectives.
- A problem seen in 2 of 5 is real. A fix requested by 1 of 5 is a hypothesis.
- Players diagnose symptoms, not causes; design the fix yourself.
- Separate "confusing" (fix the teaching) from "boring" (fix the loop) from "broken" (fix the bug).

## Results and decisions

| Finding | Evidence (who, when) | Severity P0–P3 | Decision | Owner |
|---|---|---|---|---|

- Kill / keep decision: <> with the evidence.
- Changes for the next build: <three at most>.
- Next test date and question: <>.
