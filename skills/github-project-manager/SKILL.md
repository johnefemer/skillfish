---
name: github-project-manager
description: Invisible AI project manager for GitHub. Auto-discovers projects, creates rich issues, estimates work, syncs boards, and keeps your backlog alive.
---

# GitHub Project Manager

> *"Every AI coding agent can write code, but none of them manage the project around it. I kept running into the same problem — my agents would build features but the GitHub project board was always stale. Issues were vague, estimates were missing, and there was no connection between what the agent was doing and what the board showed.*
>
> *I wanted an invisible project manager that lives inside the AI agent — one that creates rich, AI-readable issues, keeps the board honest, breaks work down like a senior engineer, and estimates with the precision of someone who's actually read the codebase.*
>
> *This skill turns any AI agent into a project management partner that keeps GitHub Projects in perfect sync with actual development work."*
>
> — **John Efemer**, creator of AI Coach

## When to Use

- Creating GitHub issues of any type (epic, feature, task, bug, chore, spike)
- Breaking down a PRD, spec, or feature description into structured issues
- Estimating work size and story points for issues
- Managing GitHub Projects v2 board fields (status, priority, size, estimate)
- Moving issues through workflow states (Backlog → Ready → In Progress → In Review → Done)
- Planning sprints or triaging the backlog
- Bootstrapping a label taxonomy for a new repository
- Generating standup reports or progress summaries
- Setting up project board configuration for the first time

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- Working directory is a git repository with a GitHub remote
- Write access to the target repository and GitHub Project
- For project board operations, ensure project scope: `gh auth refresh -s project`
- **Optional:** `gh-sub-issue` extension for native sub-issue linking (see [Sub-Issue Management](#sub-issue-management))

## Workflow

### Phase 1: Discovery & Configuration

Run this on first use or when no `.github/project-config.json` exists.

#### Step 1: Detect Repository Context

```bash
gh repo view --json owner,name,url,description
```

Extract `owner` (org or user) and `repo` name from the remote.

#### Step 2: Discover GitHub Projects

```bash
gh project list --owner {owner} --format json
```

Present the available projects to the user. Let them choose which project board to associate with this repo.

#### Step 3: Map Project Fields and Option IDs

```bash
gh project field-list {project_number} --owner {owner} --format json
```

This returns all custom fields (Status, Priority, Size, Estimate, etc.) with their field IDs and, for single-select fields, all option IDs and names. Parse and store these automatically — never hardcode IDs.

#### Step 4: Detect Project Conventions

Read these files if they exist in the repo:
- `CLAUDE.md` — AI agent instructions and coding standards
- `AGENTS.md` — Agent-specific rules and constraints
- `CONTRIBUTING.md` — Contribution guidelines

Extract: tech stack, testing framework, coding standards, file organization rules. These get injected into issue templates as contextual Technical Notes.

#### Step 5: Detect Team Members

```bash
gh api repos/{owner}/{repo}/collaborators --jq '.[].login'
```

Store team member usernames for assignment suggestions.

#### Step 6: Bootstrap Label Taxonomy

Create the full label set using `gh label create --force` (idempotent — safe to re-run).

See [Label Taxonomy & Bootstrap](#label-taxonomy--bootstrap) section for the complete set.

#### Step 7: Detect Sub-Issue Extension

Check whether the `gh-sub-issue` extension is installed:

```bash
gh extension list | grep -q "yahsan2/gh-sub-issue" && echo "available" || echo "missing"
```

If the extension is **missing**, ask the user:

> The `gh-sub-issue` extension is not installed. It enables native GitHub sub-issue linking (parent → child relationships visible in the GitHub UI). Install it now? (recommended — takes 5 seconds)

- **Yes → install:**
  ```bash
  gh extension install yahsan2/gh-sub-issue
  ```
- **No → continue with body-based fallback:** Parent/child links are embedded in issue bodies instead. All features still work.

Store the result so this check does not repeat on every operation.

#### Step 8: Write Configuration File

Save everything to `.github/project-config.json`. This file is committable so the whole team shares the same configuration.

```json
{
  "version": 1,
  "owner": "{auto-detected}",
  "repositories": [
    { "name": "{repo-name}", "label": "repo:{shortname}" }
  ],
  "project": {
    "number": "{selected}",
    "id": "{auto-discovered}",
    "title": "{auto-discovered}"
  },
  "fields": {
    "Status": {
      "id": "{auto-discovered}",
      "options": {
        "{OptionName}": "{option-id}"
      }
    },
    "Priority": {
      "id": "{auto-discovered}",
      "options": {}
    },
    "Size": {
      "id": "{auto-discovered}",
      "options": {}
    },
    "Estimate": {
      "id": "{auto-discovered}",
      "type": "number"
    }
  },
  "labels": {
    "bootstrapped": true,
    "customDomains": []
  },
  "team": ["{username1}", "{username2}"],
  "conventions": {
    "source": "CLAUDE.md",
    "techStack": "{auto-detected}",
    "testCommand": "{auto-detected}",
    "lintCommand": "{auto-detected}"
  },
  "extensions": {
    "subIssue": {
      "available": true,
      "detectedAt": "{ISO-date}"
    }
  }
}
```

Ask the user if they want to add custom domain labels (e.g., `domain:payments`, `domain:scheduling`) that reflect their product areas.

Ask if they manage multiple repositories from one project board. If yes, add additional entries to the `repositories` array.

### Phase 2: Issue Operations

Always read `.github/project-config.json` before any operation. If it does not exist, run Phase 1 first.

#### Creating Issues

Every issue follows this process:

1. **Check for duplicates** — Search existing open issues for similar titles or keywords:
   ```bash
   gh issue list --repo {owner}/{repo} --state open --json number,title --jq '.[] | "\(.number): \(.title)"'
   ```
   Warn if a potential duplicate exists. Link related issues in the new issue body.

2. **Determine issue type** — Based on user request, select the type prefix:
   - `[Epic]` — Large initiative containing sub-issues
   - `[Feature]` — New user-facing capability
   - `[Task]` — Implementation work (coding, engineering)
   - `[Bug]` — Something broken that needs fixing
   - `[Chore]` — Maintenance, refactoring, dependency updates (no user-facing change)
   - `[Spike]` — Time-boxed research or investigation

3. **Generate issue body** — Use the appropriate template from [Issue Templates](#issue-templates). Inject project conventions from `CLAUDE.md`/`AGENTS.md` into the Technical Notes section.

4. **Apply labels** — Every issue MUST have:
   - One repository label (`repo:*`)
   - At least one domain label (`domain:*`)
   - Optionally: component labels, priority labels, signal labels

5. **Create the issue:**
   ```bash
   gh issue create --repo {owner}/{repo} \
     --title "[Type] Concise, actionable title" \
     --body "$BODY" \
     --label "repo:{shortname},domain:{domain}"
   ```

6. **Add to project board:**
   ```bash
   ITEM_ID=$(gh project item-add {project_number} --owner {owner} --url {issue_url} --format json | jq -r '.id')
   ```

7. **Set project fields** (Status, Priority, Size, Estimate):
   ```bash
   # Set Status (default: Backlog)
   gh project item-edit --project-id {project.id} --id $ITEM_ID \
     --field-id {fields.Status.id} --single-select-option-id {fields.Status.options.Backlog}

   # Set Priority
   gh project item-edit --project-id {project.id} --id $ITEM_ID \
     --field-id {fields.Priority.id} --single-select-option-id {priority_option_id}

   # Set Size
   gh project item-edit --project-id {project.id} --id $ITEM_ID \
     --field-id {fields.Size.id} --single-select-option-id {size_option_id}

   # Set Estimate (story points)
   gh project item-edit --project-id {project.id} --id $ITEM_ID \
     --field-id {fields.Estimate.id} --number {points}
   ```

#### Linking Sub-Issues to Epics

Always read `extensions.subIssue.available` from `.github/project-config.json` before linking. Use the appropriate mode:

##### Mode A — Native (gh-sub-issue extension available)

```bash
# Link an existing issue as a sub-issue of the epic
gh sub-issue add {parent_number} {sub_issue_number}

# Create a brand-new sub-issue directly under the epic
gh sub-issue create --parent {parent_number} --title "[Task] Sub-issue title"

# List all sub-issues of an epic
gh sub-issue list {parent_number}
```

The relationship is stored natively in GitHub and appears in the UI. Still update the epic's `## Sub-Issues` checklist in the body — it serves as a human-readable overview even when native links exist.

##### Mode B — Body-based fallback (extension not installed)

When the extension is unavailable, encode the relationship in issue bodies:

**In the child issue body** — prepend a Parent line:
```markdown
**Parent:** #{parent_number} — {epic_title}
```

**In the epic body** — keep the `## Sub-Issues` checklist current:
```markdown
## Sub-Issues

- [ ] #{child_1} — {title}
- [ ] #{child_2} — {title}
```

Update it via:
```bash
# Fetch current body, append new sub-issue line, push update
CURRENT=$(gh issue view {parent_number} --repo {owner}/{repo} --json body -q '.body')
UPDATED="${CURRENT}
- [ ] #{child_number} — {child_title}"
gh issue edit {parent_number} --repo {owner}/{repo} --body "$UPDATED"
```

##### Discovering Sub-Issues (Mode B)

When the extension is not available, find all children of an epic by searching issue bodies:

```bash
gh issue list --repo {owner}/{repo} --state open --json number,title,body \
  | jq '.[] | select(.body | test("\\*\\*Parent:\\*\\* #{parent_number}"))'
```

#### Closing Issues

```bash
gh issue close {number} --repo {owner}/{repo}
```

Apply a resolution label if appropriate: `resolution:duplicate`, `resolution:wontfix`, `resolution:stale`, `resolution:by-design`.

#### Commenting on Issues

```bash
gh issue comment {number} --repo {owner}/{repo} --body "Update text here"
```

### Phase 3: Board Operations

#### Moving Issues Through States

```bash
# Get the item ID for an issue
ITEM_ID=$(gh project item-list {project_number} --owner {owner} --format json | jq -r '.items[] | select(.content.number == {issue_number}) | .id')

# Update status
gh project item-edit --project-id {project.id} --id $ITEM_ID \
  --field-id {fields.Status.id} --single-select-option-id {target_status_option_id}
```

#### Standard Workflow Transitions

| Transition | When |
| --- | --- |
| → Backlog | Issue created, not yet groomed |
| → Ready | Requirements clear, "Needs Clarity" section is empty |
| → In Progress | Developer assigned, work started |
| → In Review | PR opened and linked |
| → Done | PR merged, issue closed |

#### Listing Project Items

```bash
# All items
gh project item-list {project_number} --owner {owner} --format json

# Filter by status (in-memory after fetching)
gh project item-list {project_number} --owner {owner} --format json | jq '.items[] | select(.status == "In Progress")'
```

#### Assigning Issues

```bash
gh issue edit {number} --repo {owner}/{repo} --add-assignee {username}
```

### Phase 4: Reporting & Insights

#### Standup Report

When asked for a standup summary:
1. List items currently `In Progress` with assignees
2. List items moved to `In Review` or `Done` recently
3. Flag items stuck in `In Progress` for more than 2 days
4. Highlight items with no assignee or missing estimates
5. Output a clean markdown summary

#### Epic Health Check

When asked about epic progress:
1. List all sub-issues with their status
2. Calculate completion percentage
3. Sum remaining story points
4. Identify blocked or stale sub-issues
5. Suggest re-prioritization if behind schedule

#### Sprint Velocity

When asked to plan a sprint:
1. Calculate average story points completed per sprint from recent `Done` items
2. List all `Ready` items sorted by priority
3. Propose a sprint backlog that fits within velocity
4. Identify dependency chains and flag blockers

## Issue Templates

### AI Developer Model Guidelines

Every issue must contain enough information for an AI coding agent to:
1. **Understand the context** — Why this issue exists and what problem it solves
2. **Know the scope** — Exactly what files, modules, or components are affected
3. **Implement correctly** — Clear technical requirements and constraints
4. **Test the work** — Verifiable acceptance criteria
5. **Surface ambiguity** — Explicit "Needs Clarity" section for open questions

### Issue Quality Checklist

Before creating any issue, verify it has:
- [ ] Clear, actionable title with type prefix
- [ ] One-sentence summary in the first line of body
- [ ] Repository label applied
- [ ] Domain label(s) applied (at least one)
- [ ] Scope definition (in/out)
- [ ] File/module paths where changes are expected
- [ ] Testable acceptance criteria (not vague "should work")
- [ ] Technical constraints from project conventions (CLAUDE.md/AGENTS.md)
- [ ] "Needs Clarity" section (even if empty)

### [Epic] Template

```markdown
> **One-line summary:** {What this epic delivers in one sentence}

## Overview

{2-3 sentence description of what this epic accomplishes and why it matters}

## Scope

### In Scope
- {Specific capability 1}
- {Specific capability 2}

### Out of Scope
- {What this epic does NOT include}
- {Deferred to future work}

## Dependencies

| Dependency | Status | Notes |
| --- | --- | --- |
| #{issue} | Open/Closed | {Why needed} |

## Acceptance Criteria

- [ ] {Specific, testable criterion 1}
- [ ] {Specific, testable criterion 2}
- [ ] All tests pass
- [ ] No linting errors

## Technical Notes

{Auto-injected from CLAUDE.md/AGENTS.md: tech stack, coding standards, file organization}

## Affected Files/Modules

| Path | Action | Description |
| --- | --- | --- |
| `src/...` | Create/Modify | {Description} |

## Sub-Issues

- [ ] #{sub-1} — {Title}
- [ ] #{sub-2} — {Title}

## Success Metrics

- {How to measure if this epic succeeded}

## Needs Clarity

- [ ] {Question 1}

If no questions: "None — requirements are clear."
```

### [Feature] Template

```markdown
> **One-line summary:** {What this feature enables}

## User Story

**As a** {type of user}
**I want** {capability}
**So that** {benefit/outcome}

## Scope

### In Scope
- {Deliverable 1}

### Out of Scope
- {Not included}

## Acceptance Criteria

- [ ] {User-facing criterion}
- [ ] {API response criterion}
- [ ] Tests added for new functionality
- [ ] Documentation updated (if public API)

## Technical Specification

### Files to Modify/Create

| Path | Action | Description |
| --- | --- | --- |
| `src/...` | Create | {New component/service} |

### API Contract (if applicable)

```http
{METHOD} /api/v1/{resource}
```

## Technical Notes

{Auto-injected from CLAUDE.md/AGENTS.md}

## UI/UX Notes

{Wireframe description, design reference, or "N/A — no UI changes"}

## Needs Clarity

- [ ] {Question}

If no questions: "None — requirements are clear."
```

### [Task] Template

```markdown
> **One-line summary:** {What this task delivers}

## Parent

{Link to parent epic if applicable, or "Standalone task"}

## Description

{2-3 sentences describing what needs to be done and why}

## Scope

### In Scope
- {Specific deliverable}

### Out of Scope
- {Not included}

## Acceptance Criteria

- [ ] {Specific, testable criterion}
- [ ] Tests written and passing
- [ ] Code formatted per project standards

## Files to Modify

| Path | Action | Description |
| --- | --- | --- |
| `src/...` | Create/Modify | {What changes} |

## Technical Notes

{Auto-injected from CLAUDE.md/AGENTS.md}

## Testing Requirements

| Test Type | File | Description |
| --- | --- | --- |
| Unit | `tests/...` | {What to test} |
| Integration | `tests/...` | {What to test} |

## Suggested Approach

1. {Step 1}
2. {Step 2}

## Definition of Done

- [ ] Code compiles with no errors
- [ ] Acceptance criteria met
- [ ] Tests passing
- [ ] Code formatted and linted

## Needs Clarity

If no questions: "None — requirements are clear."
```

### [Bug] Template

```markdown
> **One-line summary:** {What's broken in one sentence}

## Bug Summary

| Field | Value |
| --- | --- |
| Severity | Critical / High / Medium / Low |
| Component | {Affected module or path} |
| Version | {Version or git commit} |

## Steps to Reproduce

1. {Step 1}
2. {Step 2}
3. {Observe: ...}

## Expected Behavior

{What SHOULD happen}

## Actual Behavior

{What ACTUALLY happens}

```
{Exact error message or unexpected output}
```

## Environment

| Field | Value |
| --- | --- |
| Environment | local / staging / production |
| OS / Runtime | {Relevant version info} |

## Root Cause Analysis

**Suspected cause:** {Hypothesis if investigated}

**Relevant code:** `{file:line}` — {Why suspect}

## Proposed Fix

{Description of fix approach, or "Needs investigation"}

## Workaround

{Temporary workaround, or "None known"}

## Acceptance Criteria for Fix

- [ ] Bug no longer reproduces with steps above
- [ ] Regression test added
- [ ] No new linting errors
- [ ] Related edge cases tested

## Needs Clarity

If no questions: "None — bug is well-defined."
```

### [Chore] Template

```markdown
> **One-line summary:** {What maintenance this performs}

## Motivation

{Why this maintenance task matters now — what breaks or degrades if deferred}

## Impact if Deferred

{Consequences of not doing this: tech debt growth, security risk, performance degradation}

## Scope

### In Scope
- {Deliverable 1}

### Out of Scope
- {Not included}

## Acceptance Criteria

- [ ] {Specific criterion}
- [ ] All existing tests still pass
- [ ] No regressions introduced

## Files to Modify

| Path | Action | Description |
| --- | --- | --- |

## Technical Notes

{Auto-injected from CLAUDE.md/AGENTS.md}

## Needs Clarity

If no questions: "None — requirements are clear."
```

### [Spike] Template

```markdown
> **One-line summary:** {What question this investigation answers}

## Questions to Answer

1. {Primary question}
2. {Secondary question}

## Time Box

{Recommended: 2-4 hours. Maximum: 1 day.}

## Context

{Why we need to investigate this — what decision depends on the outcome}

## Expected Output

- [ ] {Document/ADR summarizing findings}
- [ ] {Proof of concept (if applicable)}
- [ ] {Recommendation with trade-offs}

## Constraints

{Known constraints or boundaries for the investigation}

## Needs Clarity

If no questions: "None — investigation scope is clear."
```

## Work Estimation Guide

When estimating issue size, use this framework:

| Size | Story Points | Time Guide | Examples |
| --- | --- | --- | --- |
| XS | 1 | < 2 hours | Config change, small fix, typo, env variable |
| S | 2 | 2-4 hours | Single function, one-file change, simple endpoint |
| M | 3 | 4-8 hours | Feature component, multi-file change, new service |
| L | 5 | 1-2 days | Complex feature, new module, significant refactor |
| XL | 8 | 2-5 days | Major subsystem, cross-cutting change, new integration |

### Estimation Process

1. Read the issue scope and acceptance criteria
2. Identify affected files by scanning the codebase
3. Assess complexity: number of files, cross-module dependencies, test requirements
4. Compare against similar past issues if available
5. Assign Size and Story Points
6. If larger than XL, recommend breaking into smaller issues

### Estimation Calibration

Over time, compare estimates vs actuals (time from In Progress to Done). If your M-sized tasks consistently take 2 days instead of 4-8 hours, recalibrate the scale for this project.

## Label Taxonomy & Bootstrap

### Label Groups

#### Type Labels (Green family: `#0E8A16`)
```bash
gh label create "type:epic" --description "Large initiative spanning multiple features" --color "0E8A16" --force
gh label create "type:feature" --description "New user-facing capability" --color "1A7F37" --force
gh label create "type:task" --description "Implementation work" --color "2DA44E" --force
gh label create "type:bug" --description "Something broken that needs fixing" --color "3FB950" --force
gh label create "type:chore" --description "Maintenance, refactoring, dependency updates" --color "56D364" --force
gh label create "type:spike" --description "Time-boxed research or investigation" --color "7EE787" --force
```

#### Priority Labels (Red gradient)
```bash
gh label create "priority:p0-critical" --description "Production down, security issue, blocks release" --color "B60205" --force
gh label create "priority:p1-high" --description "Current milestone blocker, important fix" --color "D93F0B" --force
gh label create "priority:p2-medium" --description "Scheduled work, standard priority" --color "E99D42" --force
gh label create "priority:p3-low" --description "Nice-to-have, backlog candidate" --color "C2E0C6" --force
```

#### Domain Labels (Purple family: `#7057FF`)
```bash
gh label create "domain:frontend" --description "Client-side UI, components, pages" --color "7057FF" --force
gh label create "domain:backend" --description "Server-side logic, services, APIs" --color "8B6FE8" --force
gh label create "domain:api" --description "REST/GraphQL API endpoints and contracts" --color "6E5494" --force
gh label create "domain:infra" --description "Infrastructure, CI/CD, deployment" --color "9B8CDB" --force
gh label create "domain:docs" --description "Documentation, guides, READMEs" --color "B4A7E5" --force
```

During setup, ask the user for custom domain labels specific to their product (e.g., `domain:payments`, `domain:scheduling`, `domain:auth`). Create them with the purple color family.

#### Component Labels (Blue family: `#1D76DB`)
```bash
gh label create "component:api" --description "REST API, controllers, routes" --color "1D76DB" --force
gh label create "component:service" --description "Business logic, services, managers" --color "0969DA" --force
gh label create "component:model" --description "Data layer, models, migrations" --color "218BFF" --force
gh label create "component:ui" --description "User interface, components, layouts" --color "54AEFF" --force
gh label create "component:test" --description "Test infrastructure, fixtures, mocks" --color "79C0FF" --force
gh label create "component:config" --description "Configuration, environment, settings" --color "A5D6FF" --force
```

#### Signal Labels (Mixed colors for visual distinction)
```bash
gh label create "needs:triage" --description "Requires prioritization or clarification" --color "D4C5F9" --force
gh label create "needs:design" --description "Requires UX/UI design before implementation" --color "D4C5F9" --force
gh label create "needs:clarity" --description "Has open questions that block implementation" --color "D4C5F9" --force
gh label create "needs:review" --description "Ready for code review or product review" --color "D4C5F9" --force
gh label create "blocked" --description "Waiting on external dependency or decision" --color "B60205" --force
gh label create "security" --description "Security-related issue, fast-track triage" --color "B60205" --force
gh label create "breaking-change" --description "API or contract change requiring client updates" --color "B60205" --force
gh label create "performance" --description "Performance optimization or regression" --color "FEF2C0" --force
gh label create "tech-debt" --description "Technical debt reduction" --color "FEF2C0" --force
```

#### Size Labels (Yellow family: `#FBCA04`)
```bash
gh label create "size:xs" --description "< 2 hours, 1 story point" --color "FEF2C0" --force
gh label create "size:s" --description "2-4 hours, 2 story points" --color "FBCA04" --force
gh label create "size:m" --description "4-8 hours, 3 story points" --color "E4B819" --force
gh label create "size:l" --description "1-2 days, 5 story points" --color "D4A72C" --force
gh label create "size:xl" --description "2-5 days, 8 story points" --color "B08C19" --force
```

#### Resolution Labels (Gray: `#CFD3D7`)
```bash
gh label create "resolution:duplicate" --description "Already tracked in another issue" --color "CFD3D7" --force
gh label create "resolution:wontfix" --description "Intentionally not addressing" --color "CFD3D7" --force
gh label create "resolution:stale" --description "No activity, auto-closed" --color "CFD3D7" --force
gh label create "resolution:by-design" --description "Working as intended" --color "CFD3D7" --force
```

### Minimum Required Labels Per Issue

| Required | Label Type |
| --- | --- |
| MUST have | Title type prefix (`[Epic]`, `[Feature]`, etc.) |
| MUST have | At least one domain label (`domain:*`) |
| SHOULD have | Component label (`component:*`) |
| SHOULD have | Size label (`size:*`) for tasks and sub-issues |

## Advanced Workflows

### PRD-to-Issues Pipeline

When the user provides a PRD or feature spec:

1. **Parse** — Read the document, identify feature areas and requirements
2. **Check for duplicates** — Search existing issues to avoid double-creation
3. **Create milestones** — One per PRD phase or release:
   ```bash
   gh api repos/{owner}/{repo}/milestones -f title="Phase 1: {Title}" -f description="{Description}"
   ```
4. **Create Epics** — One `[Epic]` per feature area, with priority set
5. **Create Sub-Issues** — Break each epic into `[Task]` issues with size estimates
6. **Link everything** — Connect sub-issues to epics, assign milestones
7. **Add to board** — Set all project fields (Status=Backlog, Priority, Size, Estimate)
8. **Summarize** — Output: "Created {N} epics, {M} tasks, estimated at {P} total story points"

### Sprint Planning Autopilot

When asked to plan a sprint:

1. Calculate team velocity from recent completed work
2. List all `Ready` items sorted by priority (P0 first)
3. Propose a sprint backlog that fits within velocity
4. Identify dependency chains — flag items that block others
5. Flag items with missing estimates or unclear requirements
6. Move selected items to `In Progress` upon confirmation

### Triage Autopilot

When asked to triage the backlog:

1. List all issues with `needs:triage` label or no priority set
2. For each issue, suggest: priority, size, domain labels, component labels
3. Flag issues with vague acceptance criteria
4. Flag potential duplicates
5. Present suggestions for user confirmation before applying

### Epic Health Monitor

When asked about epic progress:

1. **Discover sub-issues** using the active mode:
   - Native: `gh sub-issue list {parent_number}`
   - Fallback: `gh issue list` filtered by `**Parent:** #{parent_number}` in body
2. List all sub-issues with status, assignee, and size
3. Calculate: total points, completed points, remaining points
4. Completion percentage with progress bar
5. Items at risk: stuck in `In Progress` > 2 days, no assignee, blocked
6. Projected completion based on current velocity
7. Recommend: re-prioritize, split large tasks, unblock dependencies

### Cross-Repo Coordination

For organizations with multiple repositories:

1. Create the primary issue in the most-affected repo
2. Apply `repo:shared` label for cross-cutting work
3. Create linked tracking issues in other repos (reference primary issue)
4. Add all issues to the same project board
5. Apply `blocked` label to dependent issues

## Personalization

### Custom Workflow States

The skill auto-discovers whatever states the project has. A team using `Todo / Doing / Testing / Shipped` gets full support — no manual mapping needed.

### Custom Domain Labels

During setup, the skill asks for project-specific domains. A SaaS product might add `domain:billing`, `domain:auth`, `domain:notifications`. An e-commerce platform might add `domain:catalog`, `domain:checkout`, `domain:fulfillment`.

### Convention-Aware Templates

Issue templates adapt to the project:
- A Go project gets: "ensure `go test ./...` passes" in acceptance criteria
- A Python project gets: "run `pytest` and `ruff check`"
- A TypeScript project gets: "run `npm test` and `npm run lint`"
- A monorepo gets: package-specific file paths and build commands

The skill reads these from `CLAUDE.md`/`AGENTS.md` — never hardcoded.

### Team-Aware Assignment

The skill learns team member patterns. When creating issues, it can suggest assignees based on who usually works on specific domains or components.

### Estimation Calibration

Compare estimates vs actuals over time. If M-sized tasks consistently take 2 days instead of 4-8 hours, suggest recalibrating the scale for this project.

## Output Format

### Issue Creation Output

```
✅ Created: [Task] Implement user session timeout (#142)
   Repository: myorg/myapp
   Labels: domain:auth, component:service, size:m
   Board: Added to "Engineering Board"
   Status: Backlog | Priority: P1 | Size: M (3 pts)
   URL: https://github.com/myorg/myapp/issues/142
```

### Epic Breakdown Output

```
📋 Epic: [Epic] User Authentication Overhaul (#140)
   🔗 Sub-issue linking: native (gh-sub-issue extension active)
   — or —
   📝 Sub-issue linking: body-based (gh-sub-issue not installed — run: gh extension install yahsan2/gh-sub-issue)

  Sub-Issues Created:
  ├── [Task] Migrate session store to Redis (#141) — S (2 pts)
  ├── [Task] Implement session timeout (#142) — M (3 pts)
  ├── [Task] Add refresh token rotation (#143) — M (3 pts)
  ├── [Task] Update auth middleware (#144) — S (2 pts)
  └── [Task] Write integration tests (#145) — M (3 pts)

  Total: 5 tasks, 13 story points
  All added to project board with Status: Backlog
```

### Standup Report Output

```
📊 Standup Report — 2024-01-15

🟢 In Progress (3)
  • #142 Implement session timeout — @dev1 (M, Day 1)
  • #156 Fix payment webhook — @dev2 (S, Day 2)
  • #160 Update API docs — @dev1 (XS, Day 1)

🔵 In Review (1)
  • #141 Migrate session store to Redis — @dev2 (PR #89)

✅ Done Since Last Standup (2)
  • #139 Set up Redis cluster — @dev1
  • #144 Update auth middleware — @dev2

⚠️ Attention
  • #156 has been In Progress for 2 days (estimated: S / 2-4 hours)
  • #143 has no assignee (Ready, P1)

📈 Velocity: 8 pts/week (last 2 weeks avg)
```

## Examples

### Example 1: Create a Bug Issue

**Input:** "Create a bug — the login page shows a blank screen on Safari after the last deploy"

**Output:** Creates issue with `[Bug]` prefix, Safari reproduction steps, environment table, and adds to project board with Priority P1, Size S.

### Example 2: Break Down a Feature

**Input:** "Break down the new notification system into tasks"

**Output:** Creates `[Epic] Notification System` with sub-issues: database schema, service layer, API endpoints, email integration, push notifications, UI components. Each sized and estimated.

### Example 3: Plan a Sprint

**Input:** "Plan the next sprint for the team"

**Output:** Reviews Ready items, calculates velocity (12 pts/week), proposes 12 points of work sorted by priority, moves to In Progress upon confirmation.

### Example 4: First-Time Setup

**Input:** "Set up project management for this repo"

**Output:** Runs full discovery, detects extension availability, creates 40+ labels, saves config, reports: "Project board 'Engineering Board' configured. 42 labels created. Sub-issue linking: native. Config saved to .github/project-config.json."

### Example 5: Create an Epic with Sub-Issues

**Input:** "Create an epic for the payment integration and break it into tasks"

**Output:** Creates `[Epic] Payment Integration (#88)`, then creates 4 sub-tasks. If extension is available, links them natively with `gh sub-issue add`. If not, adds `**Parent:** #88` to each child and updates the epic's `## Sub-Issues` checklist.

### Example 6: Check Sub-Issues

**Input:** "List all sub-issues for epic #88"

**Output:** Runs `gh sub-issue list 88` (native) or searches issue bodies for `**Parent:** #88` (fallback), then renders the health summary.

---

## Sub-Issue Management

> Native sub-issue relationships (parent → child visible in the GitHub UI) require the `gh-sub-issue` extension by [@yahsan2](https://github.com/yahsan2). This skill works fully without it — relationships are tracked in issue bodies as a fallback.

### Install the Extension

```bash
gh extension install yahsan2/gh-sub-issue
```

### Extension Commands

```bash
# Link an existing issue as a sub-issue of a parent
gh sub-issue add <parent-issue-number> <sub-issue-number>

# Create a new sub-issue directly under a parent
gh sub-issue create --parent <parent-issue-number> --title "Sub-issue title"

# List all sub-issues of a parent issue
gh sub-issue list <parent-issue-number>
```

You can use issue numbers or full URLs interchangeably:
```bash
gh sub-issue add 42 71
gh sub-issue add https://github.com/org/repo/issues/42 https://github.com/org/repo/issues/71
```

### Capability Detection

The skill checks for the extension on first run and stores the result in `.github/project-config.json` under `extensions.subIssue.available`. To re-check (e.g., after installing the extension mid-project), delete the key from config and re-run any operation — detection runs automatically.

### Fallback Behavior (No Extension)

When `extensions.subIssue.available` is `false`:

| Operation | Behavior |
| --- | --- |
| Link child to parent | Prepend `**Parent:** #N — {title}` to child issue body |
| Create child under parent | Create issue normally, then add Parent line to body |
| List sub-issues of epic | `gh issue list` filtered by `**Parent:** #N` in body |
| Epic health check | Body-search discovery, same health metrics |

The body-based approach is fully functional — epic health reports, sprint planning, and the PRD pipeline all work. The only difference is the relationship is not visible as a native GitHub UI link.

---

## Good to Know

### Sub-Issues Are Not Native to the GitHub CLI

The `gh` CLI does not include built-in sub-issue commands. GitHub added sub-issue support to the UI in 2024, but `gh` CLI commands like `gh issue edit --add-sub-issue` are **not available** in the current stable release. Native sub-issue linking from the command line requires the community extension.

### The gh-sub-issue Extension

- **Repo:** [https://github.com/yahsan2/gh-sub-issue](https://github.com/yahsan2/gh-sub-issue)
- **Author:** [@yahsan2](https://github.com/yahsan2) — community-maintained GitHub CLI extension
- **Install:** `gh extension install yahsan2/gh-sub-issue`
- **Verify install:** `gh extension list` (look for `yahsan2/gh-sub-issue`)
- **Update:** `gh extension upgrade gh-sub-issue`

> 💡 **Tip by [@johnefemer](https://github.com/johnefemer):** Install `gh-sub-issue` at the start of every new project. The native parent→child relationship in the GitHub UI makes epic tracking significantly clearer — sub-issues appear directly on the parent issue page, progress rolls up automatically, and reviewers can see at a glance what belongs to what. If you're managing multiple epics in a sprint, the visual hierarchy is worth the 5-second install.

### Body-Based Linking Is Durable

Even when you use native linking via the extension, this skill also maintains the `## Sub-Issues` checklist in the epic body. This means:
- The relationship is visible even in tools that don't render native sub-issue UI
- You get a human-readable task list right in the issue description
- If the extension is ever unavailable, the fallback works immediately with no data loss

### Project Config Caches Extension State

To avoid running `gh extension list` on every operation (slow over many issues), the detection result is stored in `.github/project-config.json`. This file is safe to commit — team members who install the extension later just need to update the `extensions.subIssue.available` field to `true`, or delete it to trigger auto-detection.

### Migrating from Body-Based to Native Linking

If you started a project without the extension and later install it, you can retroactively link existing issues:

```bash
# For each sub-issue listed in the epic body, run:
gh sub-issue add {parent_number} {child_number}
```

The body-based `**Parent:**` lines and epic checklists remain as-is — they coexist harmlessly with native links and provide redundant visibility.
