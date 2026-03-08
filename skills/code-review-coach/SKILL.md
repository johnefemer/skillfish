---
name: code-review-coach
description: Structured code review with coaching feedback. Use when reviewing PRs, assessing code quality, or mentoring developers on best practices.
---

# Code Review Coach

Provide structured, educational code reviews that teach while reviewing.

## When to Use

- Reviewing pull requests or code changes
- Assessing code quality for a file or module
- Mentoring developers on patterns and anti-patterns

## Workflow

1. **Scan** — Read the code changes or target files
2. **Categorize** — Group findings into severity levels
3. **Coach** — For each finding, explain the *why* not just the *what*
4. **Summarize** — Provide an overall assessment with actionable next steps

## Review Categories

### Critical (must fix)
- Security vulnerabilities (injection, XSS, auth bypass)
- Data loss risks
- Race conditions or deadlocks

### Important (should fix)
- Performance issues (N+1 queries, unnecessary re-renders)
- Missing error handling at system boundaries
- Broken or missing tests for changed logic

### Suggestions (consider)
- Readability improvements
- Better naming
- Simplification opportunities

### Praise (keep doing)
- Well-structured code worth calling out
- Good test coverage
- Clean abstractions

## Output Format

```markdown
## Code Review: [file/PR name]

### Summary
[1-2 sentence overall assessment]

### Critical
- **[file:line]** — [issue]. *Why it matters:* [explanation]. *Fix:* [suggestion]

### Important
- **[file:line]** — [issue]. *Why it matters:* [explanation]. *Fix:* [suggestion]

### Suggestions
- **[file:line]** — [suggestion]. *Why:* [explanation]

### Praise
- **[file:line]** — [what's good and why]

### Score: [1-10] | Verdict: [Approve / Request Changes / Needs Discussion]
```
