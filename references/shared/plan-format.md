# Plan Format

All plans are saved to `tasks/todo.md`.
If `tasks/` doesn't exist, create it. If todo.md already exists, append a new section.

---

## File Structure

```markdown
# prompt-to-pr — {MODE_EMOJI} {MODE_NAME}
**Date:** {YYYY-MM-DD HH:MM}
**Task:** {one-line description of what the user asked}
**Branch:** {planned branch name}

---

## Preflight
- Git: ✅
- Tests: ✅ (jest)
- Coverage: ✅ (nyc)
- CLAUDE.md: ⚠️ not found
- hardshell: ⚠️ not installed

## Context Summary
- Language: TypeScript / Node.js
- Framework: Express + Prisma
- Core files: src/services/user.service.ts, src/routes/auth.routes.ts
- Adjacent: src/middleware/auth.middleware.ts

## Tasks
- [ ] 1. {task description} — Risk: LOW — Est: ~20 lines
- [ ] 2. {task description} — Risk: MEDIUM — Est: ~50 lines
- [ ] 3. {task description} — Risk: LOW — Est: ~10 lines

## Test Plan
- Run existing suite before changes (baseline)
- Write new tests for: {what}
- Run suite again after changes

## Completed Tasks
(filled in during IMPLEMENT)

## Test Results
(filled in during TEST)

## Verify Summary
(filled in during VERIFY)

## Session State
(filled in if session is interrupted)

## Lessons Learned
(filled in after PR or on errors)
```

---

## Task Entry Format

Each task must have:
- Sequential number
- Clear action verb: "Add", "Create", "Modify", "Remove", "Extract", "Fix"
- Target file or module
- Risk level: LOW / MEDIUM / HIGH
- Estimated size: ~N lines affected

```markdown
- [ ] 1. Add `sendVerificationEmail()` to src/services/email.service.ts — Risk: LOW — Est: ~30 lines
- [ ] 2. Modify `registerUser()` in src/services/user.service.ts to call email service — Risk: MEDIUM — Est: ~15 lines
- [ ] 3. Add `/verify-email` route to src/routes/auth.routes.ts — Risk: LOW — Est: ~20 lines
- [ ] 4. Add `emailVerified` field to User model in prisma/schema.prisma — Risk: HIGH — Est: schema migration
```

---

## Risk Levels

| Risk | Meaning | What to do |
|---|---|---|
| LOW | Additive change, no existing code touched | Proceed normally |
| MEDIUM | Modifies existing logic, behavior may change | Run tests after this specific task |
| HIGH | Schema changes, public API changes, security-sensitive | Pause, explain impact, get explicit micro-approval |

For HIGH risk tasks, display before executing:
```
⚠️ HIGH RISK — Task 4 involves a schema migration.
This will require a database migration and may be irreversible.
Confirm to continue with this task: yes / skip / abort
```

---

## Session State Format

Written when session is interrupted or context hits 90%:

```markdown
## Session State
- Mode: 🚀 New Feature
- Status: INTERRUPTED at phase 3/6
- Last completed task: [x] Task 2
- Next task: Task 3 — "Add /verify-email route"
- Files modified so far: src/services/email.service.ts, src/services/user.service.ts
- Files still needed: src/routes/auth.routes.ts, prisma/schema.prisma
- Resume prompt: `resume prompt-to-pr`
- Saved: {timestamp}
```

---

## Lessons Learned Format

Written after PR creation or after correcting an error:

```markdown
## Lessons Learned
- {date}: {what went wrong or what worked well} → {rule added}
  Example: Prisma schema changes require `prisma generate` after migration, not just `migrate dev`
```

These accumulate over time and become project-specific knowledge.
If CLAUDE.md exists, suggest adding recurring lessons there.
