# Development Process

How work moves from the backlog to merged code on this project. This is the
day-to-day workflow; `AGENTS.md` covers stack and coding conventions, and
`_docs/plan.md` holds the scope.

## One task at a time

Work is organised as small tasks in `_docs/tasks.md`, mirrored as GitHub issues
(#1–#15). Each task is sized to finish in a single session and is independent
enough to pick up without reading the others. Take the lowest-numbered open task
that is unblocked, unless there's a reason to reorder.

## The loop for each task

1. **Pick the issue.** Read its Goal and Description. If the scope is unclear,
   clarify before starting rather than guessing.
2. **Branch.** Create a short-lived branch off `main`, named for the issue —
   for example `project-setup` or `feat/chore-model`.
3. **Write a failing test first.** Capture the intended behaviour as a test that
   fails, then write the minimum code to make it pass. Task 1 establishes the
   test suite that makes this possible.
4. **Implement.** Keep the change scoped to this one task. If a model changes,
   include its migration in the same commit.
5. **Run the full test suite.** Everything must be green before you open a pull
   request — no failing or skipped tests.
6. **Open a pull request.** Reference the issue (e.g. "Closes #7") so it links
   and closes on merge. Keep the PR focused on the single task.
7. **Review and merge.** Once the PR is approved and checks pass, merge to
   `main` and delete the branch.

## Commits

- Small, logical commits with clear messages in the imperative mood
  ("Add chore model", not "added chore model").
- Reference the issue number where it helps (e.g. `#7`).
- Never commit secrets; configuration comes from environment variables and
  `.env` is git-ignored.

## Definition of done

A task is done when:

- The Goal in its issue is met.
- New behaviour is covered by tests, and the whole suite passes.
- Any model change ships with its migration.
- Access rules are respected and tested (parent-only actions reject children;
  members touch only their own data).
- The PR is merged and the issue is closed.

## Branches

- `main` is always in a working, tested state.
- Feature work happens on short-lived branches and merges back via PR.
- Avoid long-running branches; prefer finishing and merging one task before
  starting the next.
