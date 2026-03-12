# BMAD Agents Reference

BMAD v6.2 agent configuration and phase transition reference for the `saas-architect` skill.

## Installation

```bash
npx bmad-method@latest install
```

## Agent Roles

| Agent | Phase | Responsibility |
|-------|-------|---------------|
| Analyst | 1 | Brief validation, requirements extraction |
| PM | 2 | PRD authoring, user stories, acceptance criteria |
| Architect | 3 | System design, ADRs, tech stack decisions |
| Developer | 4 | Implementation, code generation |
| QA | 5 | Test strategy, acceptance gates |

## Phase Transitions

- **Analyst → PM:** Validated requirements doc signed off
- **PM → Architect:** PRD complete with all epics defined
- **Architect → Developer:** Architecture doc + ADR log complete
- **Developer → QA:** Feature implementation complete
- **QA → Done:** All acceptance criteria met

Refer to the [BMAD documentation](https://github.com/bmad-method/bmad-method) for full configuration.
