# Household Chores Tracker

A family web application for managing shared household chores. Parents assign
chores to family members, chores can recur on a schedule, and completed work is
verified by a parent before points are awarded. Each member signs in with their
own account.

The agreed scope lives in [`_docs/plan.md`](./_docs/plan.md); the way the work
was carried out (the PM → Engineer → QA loop) is in
[`_docs/process.md`](./_docs/process.md).

## Status

**v1 complete.** All planned v1 features are built, tested, and merged to
`main` (52 passing tests). Phase-2 items remain out of scope (see below).

## Features

- **Accounts and roles** — each family member signs in; users are either a
  **parent** (admin) or a **child** (member).
- **Households** — members belong to a household; all chores and points are
  scoped to it, so families never see each other's data.
- **Assign chores** — a parent creates a chore and assigns it to a household
  member; chores carry a title, description, point value, and recurrence.
- **Do and verify** — a member marks their chore done (via HTMX, no page
  reload); it then awaits a parent's verification. Points are credited only
  once a parent approves.
- **Points tally** — each member's total is derived from their verified chores
  (so it can't drift or double-count).
- **Recurring chores** — daily or weekly chores spawn their next occurrence when
  verified.
- **Auth-aware header** — navigation, the signed-in member's name, and logout;
  parent-only links appear only for parents.

## Tech stack

- **Python 3.10+** with **Django 5.2**, server-rendered templates.
- **HTMX** (vendored under `static/`) for partial page updates — no separate
  front-end framework.
- **uv** for dependency and environment management (`uv.lock` is committed).
- **SQLite** for local development; the styling is a single hand-written CSS
  file (`static/css/app.css`), no framework and no build step.

## Getting started

Requires [uv](https://docs.astral.sh/uv/). From the project root:

```
uv sync                                  # create the environment, install deps
uv run python manage.py migrate          # set up the database
uv run python manage.py seed_demo        # load a demo household (optional)
uv run python manage.py runserver        # http://127.0.0.1:8000
```

Then open http://127.0.0.1:8000 and sign in at `/login/`. The demo seed creates
two accounts (password `demo12345` for both):

- **demo_parent** — create/assign chores and verify completed ones.
- **demo_child** — see assigned chores and mark them done.

`seed_demo` is idempotent — re-running resets the demo data without duplicating.

## Pages

| Path | Who | What |
| --- | --- | --- |
| `/` | anyone | Public landing page |
| `/login/`, `/logout/` | anyone | Sign in / out |
| `/dashboard/` | members | Signed-in landing |
| `/chores/` | members | Your assigned chores (mark done) |
| `/chores/new/` | parents | Create and assign a chore |
| `/chores/verify/` | parents | Approve chores awaiting verification |
| `/members/new/` | parents | Add a family member |
| `/household/` | members | Household members |
| `/tally/` | members | Points per member |

## Testing

```
uv run python manage.py test
```

## Project docs

- [`_docs/plan.md`](./_docs/plan.md) — scope and v1 definition
- [`_docs/process.md`](./_docs/process.md) — development process and roles
- [`_docs/tasks.md`](./_docs/tasks.md) — the task backlog
- [`_docs/team/`](./_docs/team) — PM, engineer, and QA role definitions

## Deferred to Phase 2

- Reward catalogue and points redemption
- A richer points dashboard and leaderboard
- AI / agent features (natural-language entry, smart reminders, fairness
  suggestions)
