I updated the vault to reflect the week-of-13-Oct messages and decisions. Summary of changes (what I changed and where):

Added meeting note
- vault/Fernwork HQ/Meetings/Weekly sync 2026-10-13.md
  - Recorded attendees and the meeting items (public launch recap, SMS provider decision, Priya action for SMS templates, Vonage rollout stop, support-tool revisit, receptionist request for per-practitioner colours).

New decisions
- vault/Fernwork HQ/Decisions/Decision - SMS reminder provider is Sinch.md
  - Decided 2026-10-13: switch SMS reminders to Sinch (effective 2026-11-01). Replaces Decision - SMS reminder provider is Vonage.
- vault/Fernwork HQ/Decisions/Decision - Product analytics vendor is PostHog Cloud (EU).md
  - Decided 2026-10-14: switch to PostHog Cloud (EU). Replaces PostHog self-hosted.
- vault/Fernwork HQ/Decisions/Decision - Release cadence is twice-weekly (Tue & Thu).md
  - Decided 2026-10-15: ship Tue & Thu (still behind feature flags). Replaces prior continuous/weekly decisions.
- vault/Fernwork HQ/Decisions/Decision - Investor update cadence is monthly (with metrics dashboard link).md
  - Decided 2026-10-16: investor updates return to monthly; keep the metrics-dashboard link.
- vault/Fernwork HQ/Decisions/Decision - Design system is shadcn_ui.md
  - Decided 2026-10-16: replace Tailwind UI kit with shadcn/ui.

Updated task statuses and notes
- Cancelled / updated Vonage rollout
  - vault/Fernwork HQ/Work/Tasks/Task - Roll out sms reminder provider (Vonage).md
    - status: cancelled
    - Added note: rollout stopped 2026-10-13 (Vonage out); link to new Sinch decision.
- Added Sinch rollout tasks
  - vault/Fernwork HQ/Work/Tasks/Task - Roll out sms reminder provider (Sinch).md (todo, owner: Kenji)
  - vault/Fernwork HQ/Work/Tasks/Task - Update billing and docs for sms reminder provider (Sinch).md (todo, owner: Daniel)
- Product analytics tasks
  - vault/Fernwork HQ/Work/Tasks/Task - Roll out product analytics vendor (PostHog self-hosted).md
    - status: cancelled, note added: replaced by PostHog Cloud decision (2026-10-14).
  - vault/Fernwork HQ/Work/Tasks/Task - Roll out product analytics vendor (PostHog Cloud, EU).md (in_progress, owner: Sofia)
  - vault/Fernwork HQ/Work/Tasks/Task - Update billing and docs for product analytics vendor (PostHog Cloud).md (todo, owner: Sofia)
- Onboarding rollout
  - vault/Fernwork HQ/Work/Tasks/Task - Roll out onboarding flow (concierge onboarding call before account creation).md
    - status changed to completed; note: completed 2026-10-15 (Kenji confirmed).
- Dark mode
  - vault/Fernwork HQ/Work/Tasks/Task - Dark mode for day view.md
    - added (in_progress, owner: Kenji). Note: day view dark mode is in beta as of 2026-10-15.
- Release cadence tasks
  - vault/Fernwork HQ/Work/Tasks/Task - Update billing and docs for release cadence (twice-weekly Tue & Thu).md (in_progress, owner: Sofia) — new
  - vault/Fernwork HQ/Work/Tasks/Task - Prepare customer comms for release cadence (twice-weekly Tue & Thu).md (in_progress, owner: Daniel) — new
  - (Existing weekly/continuous release tasks left as historical/completed where appropriate; the new decision replaces them.)
- Investor updates
  - vault/Fernwork HQ/Work/Tasks/Task - Roll out investor update cadence (fortnightly ...).md
    - status: cancelled (cancelled 2026-10-16 per Brightpath request)
  - vault/Fernwork HQ/Work/Tasks/Task - Roll out investor update cadence (monthly email update on the first Monday).md
    - status changed to in_progress (reinstated; owner: Priya). Note about keeping metrics dashboard link.
- Design system tasks
  - vault/Fernwork HQ/Work/Tasks/Task - Document design system (Tailwind UI kit).md
    - status: cancelled (replaced by shadcn/ui)
  - vault/Fernwork HQ/Work/Tasks/Task - Document design system (shadcn_ui).md
    - added (in_progress, owner: Priya)
- SMS templates task
  - vault/Fernwork HQ/Work/Tasks/Task - Redesign SMS reminder templates for Sinch.md
    - added (in_progress, owner: Priya; due 2026-10-30) per weekly action.
- Support tool follow-up
  - vault/Fernwork HQ/Work/Tasks/Task - Review Plain pricing and revisit support tool decision in December.md
    - added (todo, owner: Maya) per meeting (revisit in December).
- Receptionist request
  - vault/Fernwork HQ/Work/Tasks/Task - Investigate per-practitioner calendar colours.md
    - added (todo, unassigned). Note: several receptionists requested this (raised 2026-10-13).

Minor consistency fixes
- Adjusted a few task/decision links and titles so wikilinks resolve (e.g. decision filename/title normalization for shadcn_ui).

If you want, I can:
- assign owners for the unassigned calendar-colours investigation,
- set explicit due dates for the new rollout and docs tasks,
- create a short weekly summary email draft for pilot clinics about the release cadence change and PostHog/Post analytics change.

Which of those would you like next?