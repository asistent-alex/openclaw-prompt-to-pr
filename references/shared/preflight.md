# Preflight Checks

Run all checks in order before any workflow starts.
Report results as a single block, then decide: continue or STOP.

---

## Check 1 — Git

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

- ✅ Pass → continue
- ❌ Fail → **HARD STOP**

Message to user:
```
🔴 STOP — Git not initialized.

This project has no Git repository. prompt-to-pr requires Git
for branch management, commits, and PR creation.

To fix:
  git init
  git add .
  git commit -m "chore: initial commit"

Then restart prompt-to-pr.
```

---

## Check 2 — Test suite

Look for any of the following (in order of priority):

| Signal | Detected as |
|---|---|
| `package.json` with `"test"` script | Node/JS test suite |
| `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, `setup.cfg` | Python/pytest |
| `go test ./...` runnable | Go test suite |
| `Makefile` with `test` target | Generic make-based |
| `*.test.*`, `*.spec.*`, `tests/`, `__tests__/` directory | Test files present |
| `cargo test` runnable | Rust |

- ✅ Any detected → continue
- ❌ None detected → **HARD STOP**

Message to user:
```
🔴 STOP — No test suite detected.

prompt-to-pr requires at least a minimal test suite. Without tests,
there's no safety net for changes and no way to verify fixes.

Minimum to get started:
  # Node.js
  npm init -y && npm install --save-dev jest
  # Add to package.json: "test": "jest"

  # Python
  pip install pytest && mkdir tests && touch tests/__init__.py

  # Go — already built in, just create *_test.go files

Add at least one smoke test, then restart prompt-to-pr.
```

---

## Check 3 — Coverage tool (soft)

Check if a coverage tool exists (nyc, c8, pytest-cov, go cover, etc.).

- ✅ Found → note it for Test Coverage mode
- ❌ Not found → soft warning, only relevant if using 🧪 Test Coverage mode

```
🟡 WARNING — No coverage tool detected.
Test Coverage mode will run tests but cannot generate a coverage report.
Install a coverage tool to get gap analysis. Continuing.
```

---

## Check 4 — CLAUDE.md (soft)

```bash
ls CLAUDE.md 2>/dev/null || ls .claude/CLAUDE.md 2>/dev/null
```

- ✅ Found → read it for project conventions before context scan
- ❌ Not found → soft warning

```
🟡 WARNING — No CLAUDE.md found.
Project-specific conventions won't be loaded. Continuing with defaults.
Consider creating CLAUDE.md to persist conventions across sessions.
```

---

## Check 5 — Repo discovery (soft)

If the user hasn't specified a repo (via `--repo` or in their prompt), scan for candidate repos:

1. **Workspace git repos** — check if the current workspace has a `.git` directory
2. **Installed skill repos** — scan `~/.openclaw/skills/` and `~/.npm-global/lib/node_modules/openclaw/skills/` for directories with `.git`
3. **GitHub repos** — if `gh` CLI is available, list recent repos with `gh repo list --limit 10`

If multiple repos are found, present a selection menu:
```
📂 Available repos for prompt-to-pr:

  [1] ~/workspace/my-project          (Node.js, 12 tests)
  [2] ~/.openclaw/skills/imm-romania  (Python, 8 tests)
  [3] ~/.openclaw/skills/prompt-to-pr  (Markdown, 3 tests)

  Type a number, or paste a repo path manually.
```

If exactly one repo is found (and it's the workspace), proceed silently.
If no repos found, HARD STOP (no place to work).

After selection, `cd` to the chosen repo for all subsequent checks and commands.

- ✅ Single repo → proceed silently
- ✅ Multiple repos → show menu, wait for selection
- ❌ No repos found → **HARD STOP**

```
🔴 STOP — No repos found.

prompt-to-pr needs a Git repository to work in. Either:
  - Run /ptop from inside a Git repo
  - Specify --repo <path>
  - Clone a repo first: git clone <url>
```

---

## Check 6 — hardshell (soft)

Check if `hardshell` skill is installed:
```bash
ls .claude/skills/hardshell/SKILL.md 2>/dev/null || \
ls ~/.claude/skills/hardshell/SKILL.md 2>/dev/null
```

- ✅ Found → note for IMPLEMENT and VERIFY phases
- ❌ Not found → note, use built-in checklists

```
ℹ️  hardshell not detected. Built-in quality checklists will be used.
Install hardshell for enhanced security and architecture rules.
```

---

## Preflight Summary Block

Always display before continuing:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  prompt-to-pr — PREFLIGHT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Repo             ✅  ~/.openclaw/skills/prompt-to-pr
  Git              ✅
  Test suite       ✅  (jest)
  Coverage tool    ✅  (nyc)
  CLAUDE.md        ⚠️  not found
  hardshell        ⚠️  not installed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Status: READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Or if hard stop:
```
  Status: ❌ STOPPED — see errors above
```
