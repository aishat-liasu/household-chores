# AGENTS.md

Guidance for AI coding agents working in this repository. Read this first.

## Project

Household Chores Tracker — a family web application for managing shared
household chores. Parents assign chores to family members, chores can recur on a
schedule, and completed work is verified by a parent before points are awarded.
Each member has their own account.

- The agreed scope and v1 feature set live in `_docs/plan.md`. Treat it as the
  source of truth for what v1 does and does not include.
- The task backlog lives in `_docs/tasks.md` and is mirrored as GitHub issues
  (#1–#15). Each task is sized for a single session and written to stand alone.

Do not build features deferred to Phase 2 (reward catalogue, points redemption,
dashboards/leaderboards, or any AI/agent features) unless explicitly asked.

## Tech stack

- **Python** with **Django**, server-rendered templates.
- **HTMX** for partial page updates (no separate front-end framework).
- **uv** for dependency and environment management (`uv.lock` is committed).
- **PostgreSQL** in any shared/production setting; SQLite is acceptable for
  local development and tests.

## Commands

The project is scaffolded in Task 1 (issue #1). Once set up, use uv for
everything:

- Install / sync deps: `uv sync`
- Run a command in the env: `uv run <cmd>` (e.g. `uv run python manage.py ...`)
- Run the dev server: `uv run python manage.py runserver`
- Make / apply migrations: `uv run python manage.py makemigrations` /
  `uv run python manage.py migrate`
- Run the tests: `uv run python manage.py test` (or `uv run pytest` if pytest is
  adopted)

Confirm the exact commands against the project once it exists rather than
assuming.

## Working conventions

- **Tests are required.** Every task must land with passing tests covering the
  behaviour it adds; Task 1 establishes a green test suite. Do not mark work
  done with failing or skipped tests.
- **Small, focused changes.** Work one task/issue at a time. Keep pull requests
  scoped to a single backlog item and reference its issue number.
- **Migrations.** Any model change must include its migration in the same
  change.
- **Access control matters.** Parent-only actions (creating, assigning,
  verifying) must reject child accounts; members may only touch their own data.
  Cover the forbidden paths with tests, not just the happy path.
- **Secrets.** Never commit secrets. Configuration comes from environment
  variables; `.env` is git-ignored (`.env.example` documents the shape).
- **Style.** Follow standard Django project layout and idioms. If a formatter/
  linter (e.g. ruff) is configured, run it before committing.

## Repository layout

- `_docs/plan.md` — scope and v1 definition
- `_docs/tasks.md` — the task backlog
- `README.md` — project summary
- `CLAUDE.md` — imports this file (`@AGENTS.md`)

Application code and Django project structure are added starting from Task 1.
