# Working rules for this repository

These are the owner's standing rules for any Claude session working on this repo.

## Model use (set 2026-11-11)

- **Subagents always run on Claude Opus 5.5 at xhigh effort.** With the Agent tool that is `model: "opus"` and `effort: "xhigh"`; the same for agents inside a workflow. Never start a subagent on Fable.
- **Fable is for the main conversation and orchestration only**, when the owner has the session on Fable.
- **Exception:** playtest and dry-run agents may use Fable, but only when the owner has said there is usage to spare. If unsure, use Opus.
- Do not resume a subagent that was started on Fable: start a fresh Opus one instead.
- **Remind the owner of this rule every so often**: whenever subagents are started, and in end-of-task summaries.

Why: Fable subagents use up the owner's usage allowance very quickly.

## Pushing

- Commit and push every completed change to GitHub without being asked, to both the working branch and `main` (fast-forward only). Say so if something on `main` is temporarily incomplete.

## Editing the skill

- `SKILL.md` stays short: the phase table, the full rule lists and the routing table live in `references/workflow-phases.md`, `references/decision-rules.md` and `references/INDEX.md`.
- One topic has one owner guide; other files point to it instead of restating it. New platform facts are checked against https://create.roblox.com/docs before they go in.
- The owner's house rules in `SKILL.md` are verbatim and are not reworded.
