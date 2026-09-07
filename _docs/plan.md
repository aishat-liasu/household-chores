# Household Chores Tracker — Plan & Scope

A family web application for managing shared household chores. This document
records the agreed scope for the first working version (v1) and the features
deliberately deferred to a later phase.

## Concept

Parents run the household and are responsible for creating and verifying work;
every family member — parents and children alike — has their own account and
signs in on their own device. Chores are assigned top-down by a parent, and
completing a chore earns points only once a parent has confirmed the work was
actually done.

The core motivation loop is:

**Parent assigns → child completes → parent verifies → points earned.**

## Household & Access Model

- The tool is built for a **family** (parents and children).
- **Individual logins**: each member has an account and signs in on their own
  phone or laptop.
- Parents act as administrators; children are standard members.

## Assignment Model

- **Parent-assigned**: a parent creates chores and assigns each to a specific
  family member. Assignment is top-down, with clear control.

## Motivation Model

- **Points and rewards**: completing (and verified) chores earns points, which
  are intended to build towards real-world rewards.
- In v1 the reward machinery is not yet built (see Deferred), but points are
  earned and made visible so the loop still feels rewarding.

## v1 — Must-Have Features

1. **Recurring chores** — chores can repeat on a daily or weekly schedule, not
   just one-off tasks.
2. **Chore verification** — when a member marks a chore as done, it is pending
   until a parent confirms it; points are awarded only after verification.
3. **Visible points tally** — a simple, always-visible running total of points
   per person, so completing and verifying chores feels rewarding even before
   the full reward system exists.
4. **Individual accounts** — sign-in for each member, with parent (admin) and
   child (member) roles.

## Deferred to Phase 2

- **Reward catalogue** — parents defining rewards that children redeem points
  against.
- **Points redemption** — spending accrued points on rewards.
- **Points dashboard & leaderboard** — richer views beyond the simple v1 tally.
- **AI / agent features** — natural-language chore entry, smart reminders, and
  fairness suggestions. v1 is a deliberately manual tracker; the AI layer sits
  on top of this foundation later. (This is why the project is named an "AI
  agent" even though v1 ships no AI.)

## Deliverable

A **working web application** the family can click through: create chores, mark
them done, have a parent verify them, and see points accrue.

## Open Questions / Notes

- Points are earned in v1 and shown via the visible tally, but have nowhere to
  be *spent* until the Phase 2 reward catalogue lands. This is intentional for
  the first build.
