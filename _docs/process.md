# Development Process

How work moves from the backlog to closed issues. The main session acts as an
**orchestrator** that runs three roles — PM, Engineer, and QA — as subagents.
This document defines that flow, the roles, and the practices they share.
`AGENTS.md` covers stack and coding conventions, and `_docs/plan.md` holds the
scope.

## Backlog

Work is organised as small tasks in `_docs/tasks.md`, mirrored as GitHub issues.
Each task is sized to finish in a single session and is independent enough to
pick up without reading the others. The orchestrator works through them roughly
in order, skipping any that are blocked.

## Orchestrator

The main session is the orchestrator. It launches the PM, the engineer and QA as
subagents. It does not groom, implement or test itself.

### Lifecycle

1. Pick the next open issue from the backlog.
2. PM grooms it.
3. Engineer implements it.
4. QA verifies it.
5. On FAIL, back to step 3 with the QA comment as input.
6. On PASS, close the issue.
7. Repeat until the backlog is empty.

### Rules

- Do not skip step 2.
- The engineer does not close the issue.
- QA does not fix the code, only outputs PASS or FAIL.
- The orchestrator closes the issue only after QA outputs PASS.

## Roles

- **PM** — grooms the issue into the `_docs/task-template.md` shape (Goal,
  checkable acceptance criteria, out of scope, constraints) before any code is
  written. Follows `_docs/team/pm.md`.
- **Engineer** — implements the groomed task against its acceptance criteria
  without changing them, staying inside the files and constraints the issue
  names, and writing tests as they go. Reports what was done as an issue comment,
  and flags any criterion that is wrong, impossible, or contradictory. Follows
  `_docs/team/software-engineer.md`.
- **QA** — checks each acceptance criterion against the running code, runs the
  tests and names which, and posts a PASS/FAIL verdict as an issue comment.
  Follows `_docs/team/qa-engineer.md`.

## Engineering practices

- **Branch.** Work on a short-lived branch off `main`, named for the issue. Keep
  `main` always in a working, tested state; a branch merges back once QA passes,
  not before.
- **Test-first.** Write a failing test that captures the intended behaviour, then
  the minimum code to make it pass. The whole suite must be green before QA.
- **Migrations.** Any model change ships with its migration in the same commit.
- **Commits.** Use Conventional Commits: a lowercase type prefix then a short
  imperative summary — e.g. `config: set up uv-managed Django project`,
  `feat: add chore model`, `bugfix: correct points tally` (types: `feat`,
  `fix`/`bugfix`, `config`, `chore`, `docs`, `test`, `refactor`). Reference the
  issue number where it helps. Never commit secrets; configuration comes from
  environment variables and `.env` is git-ignored.

## Definition of done

A task is done when:

- Every acceptance criterion in the groomed issue is met and can be checked by
  looking at the result.
- New behaviour is covered by tests, and the whole suite passes.
- Any model change ships with its migration.
- Access rules are respected and tested (parent-only actions reject children;
  members touch only their own data).
- Anything dropped from scope has been moved to a linked follow-up issue.
- QA has returned PASS and the orchestrator has closed the issue.
