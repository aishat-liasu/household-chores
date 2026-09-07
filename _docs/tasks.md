# Household Chores Tracker — Backlog

Stack: **Django + uv, server-rendered with HTMX** (Option 1). Scope is the v1
must-haves in `plan.md`. Each task is sized for a single session and written to
stand alone, so it can be picked up without reading the others. The numbering is
a suggested order, not a hard dependency chain.

## 1. Set up the project with a passing test
Goal: A runnable Django project managed with uv, with one test that passes.
Description: Initialise the project with uv, add Django, and create the project
skeleton with a single app. Add one trivial automated test (for example, a
health-check view returning 200) and confirm the test suite runs green. This
establishes the toolchain, test runner, and project layout everything else
builds on.

## 2. Add a base template and HTMX
Goal: A shared page layout with HTMX available across the app.
Description: Create a base HTML template with a header, a content block, and
static-asset setup, and include HTMX so later screens can update without full
page reloads. Add one simple page that extends the base to prove templating and
static files work. No feature logic — just the shared shell.

## 3. Custom user model with roles
Goal: A user model that distinguishes parents (admins) from children (members).
Description: Define a custom Django user model early, with a role field (parent
or child) or an equivalent flag. Run the initial migration and add tests
confirming a user can be created in each role. This is foundational, so it
should land before other models reference users.

## 4. Login and logout
Goal: Members can sign in and out of the app.
Description: Wire up authentication using Django's built-in auth views, with
login and logout pages that use the base template. Add a test that an
authenticated user can reach a protected page while an anonymous one is
redirected to login. Sign-up is handled separately.

## 5. Member sign-up / account creation
Goal: New family members can get an account.
Description: Provide a way to create accounts — either self sign-up or a
parent-creates-member form — capturing name, credentials, and role. Add
validation and a test that a new account is created and can then log in. Keep
the interface minimal; polish is not the goal here.

## 6. Household grouping
Goal: Members belong to a single shared household.
Description: Add a Household model and link each user to one household so chores
and points are scoped to a family rather than being global. Include a migration
and a test that members of different households cannot see each other's data.
This underpins later access control.

## 7. Chore data model
Goal: A chore can be stored with its key attributes.
Description: Create a Chore model capturing title, description, assigned member,
point value, status (for example pending / done / verified), and the fields
needed to support recurrence later. Add the migration and tests covering
creation and the default status. This is data only — no screens yet.

## 8. Parent creates and assigns a chore
Goal: A parent can create a chore and assign it to a member.
Description: Build a form and view, restricted to parents, for creating a chore
and choosing which household member it is assigned to. Add a test that a parent
can create an assigned chore and that a child cannot reach the form. Uses the
chore model and household from earlier tasks.

## 9. Member views their chores
Goal: A member sees the chores assigned to them.
Description: Add a page listing the signed-in member's chores with their current
status, showing only that person's chores and ordered sensibly. Add a test that
a member sees their own chores and not anyone else's. Read-only display — actions
come in later tasks.

## 10. Mark a chore as done
Goal: A member can mark an assigned chore as done, pending verification.
Description: Add an action (an HTMX button) that moves one of the member's own
chores into a "done, awaiting verification" state, without awarding points yet.
Add a test that the status changes and that no points are granted at this stage.
This sets up the verification step.

## 11. Parent verifies a completed chore
Goal: A parent approves a done chore, which awards its points.
Description: Give parents a view of chores awaiting verification, with an approve
action that marks the chore verified and credits the assigned member's points.
Add a test that verification awards the correct points exactly once and that only
parents can verify. Depends on the done/pending state and the points concept.

## 12. Recurring chores
Goal: Chores can repeat on a daily or weekly schedule.
Description: Extend chores with a recurrence rule and add logic that produces the
next occurrence after one is completed, or on a schedule. Add tests covering
daily and weekly recurrence generating the expected next chore. Keep it to fixed
daily and weekly patterns for v1.

## 13. Points tally
Goal: Each member's verified points are visible at a glance.
Description: Add a view that aggregates verified points per member and shows a
simple running total, optionally surfaced in the shared header. Add a test that
the tally reflects only verified chores and updates when a chore is verified. No
rewards or redemption — display only.

## 14. Role-based access control pass
Goal: Parent-only and member actions are consistently enforced.
Description: Review and lock down every view so that parent-only actions
(creating, assigning, verifying) reject children, and members can only touch
their own data. Add tests that exercise the forbidden paths and expect denials.
This is a hardening task that assumes the features already exist.

## 15. Demo seed data
Goal: A single command populates a realistic sample household.
Description: Provide a management command or fixture that creates a household
with a couple of parents, a couple of children, and a mix of one-off and
recurring chores in various states. This makes manual testing and demos quick
and repeatable. Useful for reviewing the finished v1.
