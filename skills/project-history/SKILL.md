---
name: project-history
description: Track development history across AI sessions. Maintains worklog, changelog, feature-log, and implementation-docs in .project/ files.
---

# Project History

> AI tools lose context between sessions. These files are the institutional memory.

Maintain `.project/` files as the source of truth for goals, decisions, cross-project dependencies, and effort history. Works for single-repo, mono-repo, and multi-repo workspaces.

## When This Skill Activates

1. **After completing any task** — update changelog and worklog
2. **After touching a feature** — update or create its feature-log
3. **After L/XL tasks** — update or create implementation-docs
4. **When user runs** `/update-logs`, `/worklog`, `/changelog`, `/feature-log`
5. **Before starting work on an existing feature** — read its feature-log first

## Slash Commands

| Command | What it does |
|---------|--------------|
| `/update-logs` | Full validation + update of all 4 file types |
| `/worklog` | Create/update today's goal-driven worklog |
| `/changelog` | Create/update today's outcome-focused changelog |
| `/feature-log <name>` | Create/update a feature's living document |

## File Locations

```
.project/
├── worklog/YYYY-MM-DD.md              # Daily effort tracking
├── changelog/YYYY-MM-DD.md            # Date-wise implementation log
├── feature-log/<feature-name>.md      # Living feature documents
└── implementation-docs/<task-name>.md  # Epic-level task docs
```

Full format templates and conventions: [.project/README.md](../../.project/README.md)

## Project Structure Variants

This skill adapts to any project layout. Tagging and commit-ref collection differ by structure.

### Single Repo

```
my-project/
├── .project/
│   ├── worklog/2026-03-19.md
│   ├── changelog/2026-03-19.md
│   ├── feature-log/auth-flow.md
│   └── implementation-docs/api-redesign.md
└── src/
```

- No project tags needed — single implicit project
- Commit refs: `abc1234`, `def5678`
- Collect refs: `git log --oneline --since="today"`

### Mono-Repo

```
my-monorepo/
├── .project/
│   ├── worklog/2026-03-19.md
│   ├── changelog/2026-03-19.md
│   └── feature-log/shared-auth.md
├── packages/
│   ├── api/
│   └── web/
```

- Tag entries with package paths: `[packages/api]`, `[packages/web]`
- Cross-package work: `[packages/api, packages/web]`
- Commit refs per package scope
- Collect refs: `git log --oneline --since="today" -- packages/api/`

### Multi-Repo Workspace

```
workspace/
├── .project/
│   ├── worklog/2026-03-19.md
│   ├── changelog/2026-03-19.md
│   └── feature-log/payment-flow.md
├── backend-api/
├── frontend-app/
└── shared-lib/
```

- Tag entries with repo names: `[backend-api]`, `[frontend-app]`
- Cross-repo work: `[backend-api, frontend-app, shared-lib]`
- Workspace-level: `[root]`
- Commit refs per repo: `backend-api: abc1234`
- Collect refs: `git -C backend-api log --oneline --since="today"`

## Core Rules

### 1. Goal-Driven Writing

Every entry leads with WHY, not WHAT.

Bad — activity-focused:
```
Updated channel model and added new fields to the database
```

Good — outcome-focused:
```
Enable self-service WhatsApp channel setup — businesses can now configure
WhatsApp in under 2 minutes instead of the previous 45-minute manual process
```

### 2. Project/Package Tagging (mandatory)

Tag every entry with affected projects or packages:
```
[backend-api]                          — single project/package
[backend-api, frontend-app]            — multi-project
[packages/api, packages/web]           — mono-repo packages
[root]                                 — workspace-level config
```

For single-repo projects, tags are optional — the project is implicit.

### 3. Commit References (mandatory in changelog)

Always include commit hashes per project:
```markdown
### Commits
- backend-api: `abc1234`, `def5678`
- frontend-app: `ghi9012`
```

### 4. Feature-Log Before Feature-Work

Before modifying any existing feature, read its feature-log:
```bash
cat .project/feature-log/<feature-name>.md
```
If it doesn't exist, check if it should:
```bash
grep -rl "<feature-keyword>" .project/
```

## Workflow

### After Every Task Session

```
Step 1: Collect commit refs from each touched repo/package
        git log --oneline --since="today"
        # Multi-repo:
        git -C <repo> log --oneline --since="today"
        # Mono-repo (scoped):
        git log --oneline --since="today" -- packages/<pkg>/

Step 2: Update/create changelog/YYYY-MM-DD.md
        - [project-tag] heading
        - Goal (why this change matters)
        - Categories: Added/Changed/Fixed/Removed/Security
        - Commit refs per project
        - Feature refs
        - Issue refs (GitHub issue numbers)

Step 3: Update/create worklog/YYYY-MM-DD.md
        - Goal + outcome for each task
        - T-shirt size (XS/S/M/L/XL) using standard scale
        - Project tags
        - GitHub issue reference (if applicable)
        - Daily summary table

Step 4: Update/create feature-log/<feature>.md (if feature touched)
        - New history entry with date, goal, commits
        - Update Current State if changed
        - Update Cross-Project Dependencies if changed
        - Add any new Decisions & Rationale

Step 5: Update/create implementation-docs/<task>.md (L/XL only)
        - Update checklist progress
        - Add session notes
        - Record key decisions with trade-offs
        - Link to GitHub epic if exists
```

## File Templates

### Changelog (changelog/YYYY-MM-DD.md)

```markdown
# Changelog — YYYY-MM-DD

## [project-tag]

**Goal:** {Why this change matters to users/business}

### Added
- {New capability} — {human impact}

### Changed
- {Modification} — {why changed}

### Fixed
- {Symptom that's fixed} — {root cause}

### Commits
- project-name: `abc1234`, `def5678`

### Feature Refs
- Related: feature-log/auth-flow.md

### Issue Refs
- Closes: #142, #143
```

### Worklog (worklog/YYYY-MM-DD.md)

```markdown
# Worklog — YYYY-MM-DD

## Goals
- [ ] {Goal 1}
- [x] {Goal 2 — completed}

## Tasks

### {Task Title}
- **Goal:** {What we're trying to achieve}
- **Outcome:** {What actually happened}
- **Size:** M (4-8 hours, 3 pts)
- **Projects:** [backend-api, frontend-app]
- **Issue:** #142 (if applicable)

## Blocked
- {Blocker description} — waiting on {person/decision}

## Summary

| Metric | Value |
|--------|-------|
| Tasks completed | 3 |
| Total effort | M + S + XS = 6 pts |
| Blocked items | 1 |
```

### Feature-Log (feature-log/\<feature-name\>.md)

```markdown
# Feature: {Feature Name}

**Status:** Active — Development
**Owner:** {team or person}
**Created:** YYYY-MM-DD
**GitHub Epic:** #{epic-number} (if applicable)

## Overview
{2-3 sentences describing what this feature does and why it exists}

## Current State
- {What's implemented}
- {What's pending}
- {Known limitations}

## Cross-Project Dependencies

| Project | Role | Data Flow |
|---------|------|-----------|
| backend-api | Source | Provides auth tokens via /api/auth |
| frontend-app | Consumer | Displays auth UI, stores tokens |

## Integration History

### YYYY-MM-DD — {Goal}
- **Changes:** {What changed}
- **Commits:** backend-api: `abc1234`
- **Size:** M (4-8 hours)
- **Impact:** {User/system impact}

## Decisions & Rationale

### {Decision Title}
- **Decision:** {What we decided}
- **Alternatives considered:** {What we rejected}
- **Trade-offs:** {Pros/cons of this choice}
- **Date:** YYYY-MM-DD
```

### Implementation-Doc (implementation-docs/\<task-name\>.md)

```markdown
# Implementation: {Task Name}

**Status:** In Progress
**Size:** L (1-2 days, 5 pts)
**Started:** YYYY-MM-DD
**GitHub Epic:** #{epic-number} (if applicable)

## Context & Problem
{Why this task exists — what problem it solves}

## Goal
{Desired outcome in 1-2 sentences}

## Scope

### In Scope
- {Deliverable 1}
- {Deliverable 2}

### Out of Scope
- {Explicitly excluded}

## Checklist
- [x] {Completed step}
- [ ] {Pending step}

## Decisions

### {Decision Title}
- **Decision:** {What we chose}
- **Alternatives:** {What we rejected and why}
- **Trade-offs:** {Consequences of this choice}

## Session Notes

### YYYY-MM-DD
- {What was done}
- {Blockers encountered}
- {Next steps}
```

## T-Shirt Sizing Reference

Uses the same scale as the `github-project-manager` skill for consistency across planning and history tracking.

| Size | Story Points | Time Guide | Examples |
|------|-------------|------------|---------|
| XS | 1 | < 2 hours | Config change, small fix, typo, env variable |
| S | 2 | 2-4 hours | Single function, one-file change, simple endpoint |
| M | 3 | 4-8 hours | Feature component, multi-file change, new service |
| L | 5 | 1-2 days | Complex feature, new module, significant refactor |
| XL | 8 | 2-5 days | Major subsystem, cross-cutting change, new integration |

When recording actual effort in worklog, note discrepancies for calibration:
```
**Size:** M (4-8 hours, 3 pts) — actual: ~6 hours
```

## Changelog Categories

Uses [Keep a Changelog](https://keepachangelog.com/) categories:
- **Added** — new capabilities
- **Changed** — modifications to existing behavior
- **Fixed** — bug fixes (state the symptom: "Dashboard no longer freezes")
- **Removed** — removed capabilities
- **Security** — vulnerability patches
- **Deprecated** — marked for future removal

## Feature-Log Status Values

`Draft` → `Active — Development` → `Active — Production` → `Deprecated` → `Removed`

## Implementation-Doc Status Values

`Planned` → `In Progress` → `Completed` → `Abandoned`

## Validation Checklist

After writing, verify:
- [ ] Every changelog entry has `[project-tag]` and commit refs
- [ ] Every changelog entry has a Goal line explaining human impact
- [ ] Every worklog task has a Goal, Outcome, Size, and Project tags
- [ ] Feature-logs have Status, Current State, and Integration History
- [ ] Implementation-docs have Context, Goal, Decisions with trade-offs
- [ ] Cross-project dependencies noted where applicable
- [ ] GitHub issue references included where applicable
- [ ] No credentials, tokens, or secrets in any file

## Examples

### Example 1: Single-Repo Bug Fix

**Trigger:** Completed a bug fix in a single-repo project

**changelog/2026-03-19.md:**
```markdown
## [root]

**Goal:** Prevent data loss when users refresh during checkout

### Fixed
- Cart items no longer disappear on page refresh — persisted to localStorage

### Commits
- `a1b2c3d`

### Issue Refs
- Closes: #142
```

**worklog/2026-03-19.md:**
```markdown
### Fix cart persistence bug
- **Goal:** Stop users losing cart items on refresh
- **Outcome:** Implemented localStorage persistence, tested across browsers
- **Size:** S (2-4 hours, 2 pts)
- **Projects:** [root]
- **Issue:** #142
```

### Example 2: Multi-Repo Feature

**Trigger:** Completed WhatsApp channel integration across 3 repos

**changelog/2026-03-19.md:**
```markdown
## [backend-api, frontend-app, proxy-service]

**Goal:** Enable self-service WhatsApp channel setup — reduce setup from 45 min to 2 min

### Added
- WhatsApp channel configuration API endpoints
- Self-service setup wizard in dashboard
- Webhook routing for WhatsApp messages

### Commits
- backend-api: `abc1234`, `def5678`
- frontend-app: `ghi9012`
- proxy-service: `jkl3456`

### Feature Refs
- feature-log/whatsapp-channels.md

### Issue Refs
- Part of: #88 (Epic)
- Closes: #89, #90, #91
```

**worklog/2026-03-19.md:**
```markdown
### WhatsApp channel integration
- **Goal:** Self-service WhatsApp setup for businesses
- **Outcome:** Full integration complete, tested with sandbox account
- **Size:** L (1-2 days, 5 pts) — actual: ~1.5 days
- **Projects:** [backend-api, frontend-app, proxy-service]
- **Issue:** #88 (Epic)
```

### Example 3: Mono-Repo Package Change

**Trigger:** Updated shared UI components and consuming apps

**changelog/2026-03-19.md:**
```markdown
## [packages/ui, packages/web, packages/admin]

**Goal:** Standardize form validation UX — consistent error messages across all apps

### Changed
- Form error component uses field-level validation instead of form-level
- Error messages appear inline below each field

### Commits
- `abc1234`, `def5678`, `ghi9012`
```

### Example 4: Reading Feature-Log Before Work

**Trigger:** User asks to modify the payment flow

**Actions:**
1. Check for existing feature-log:
   ```bash
   cat .project/feature-log/payment-flow.md
   ```
2. Read to understand current state, cross-project dependencies, and past decisions
3. Proceed with modification
4. Update feature-log with new history entry

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Writing "what" instead of "why" | Start every Goal with user/business impact |
| Forgetting project tags | Add `[project-tag]` to every heading |
| Missing commit refs in changelog | Run `git log --oneline --since="today"` before writing |
| Skipping feature-log read | Always check for existing feature-log before modifying a feature |
| Using different sizing scale | Use the standard scale: XS=1pt, S=2pt, M=3pt, L=5pt, XL=8pt |
| Missing GitHub issue links | Include `**Issue:** #N` when task relates to a GitHub issue |
| Secrets in logs | Never commit .env values, tokens, or credentials |

## Integration with github-project-manager

When both skills are active, they complement each other without overlap:

| Concern | github-project-manager | project-history |
|---------|----------------------|-----------------|
| **Where data lives** | GitHub Issues + Project Board | `.project/` files in repo |
| **When updated** | Issue creation, sprint planning, board sync | After task completion, daily |
| **Primary audience** | Team coordination, stakeholders | AI agents, developer memory |
| **Estimation** | Forward-looking (planning) | Backward-looking (actual effort) |
| **Commit refs** | Optional in issue bodies | Mandatory in changelog |
| **Feature lifecycle** | Issue status (Open → Closed) | Feature-log status (Draft → Production) |

**Workflow when both are active:**

```
[github-project-manager] Creates issue #142, estimates: M (3 pts)
         ↓
[developer works on task]
         ↓
[project-history] Worklog records: Size M, actual ~6 hours, Issue #142
         ↓
[project-history] Changelog records: Commits, closes #142
         ↓
[github-project-manager] Issue #142 → Done, velocity updated
```

The worklog provides "actuals" data that feeds back into sprint velocity calibration.

## Related Skills

| Skill | Relationship |
|-------|-------------|
| **github-project-manager** | Primary integration — shares sizing scale, worklog provides actuals for velocity calibration |
| **changelog-generator** | Complementary — automated changelog from commits; project-history is the manual/AI-assisted daily log |
| **git-commit-hygiene** | Prerequisite — clean commits feed into better changelogs |
| **monorepo-navigator** | Complementary — cross-package impact analysis informs project tags |
| **release-manager** | Downstream — changelog data feeds release notes |
