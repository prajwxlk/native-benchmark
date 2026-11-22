I’ve updated Fernwork’s Native workspace to reflect the 13 Oct 2026 notes. Here’s what I did, plus how it’s linked to prior records.

What I added or updated

Decisions created
- Decision - Move SMS reminders to Sinch from 1 November (Vonage decommissioned)
  - ID: 3fc8435a-2786-4221-bbde-8bc78eea4bc2
  - Body: From 1 November, move SMS reminder provider from Vonage to Sinch; Vonage is out.
  - Reason: Weekly sync decision.
  - Notes: Replaces the prior Vonage SMS decision (see supersedes below).

- Decision - Replace Tailwind UI kit with shadcn/ui as design system
  - ID: eebb4b47-8772-4869-8640-c7f9aa015282
  - Body: Replace Tailwind UI kit with shadcn/ui as the design system across products.
  - Reason: Design system refresh discussed around 2026-10-16.

- Decision - Day view dark mode in beta
  - ID: b7477f7c-c938-4780-b7b6-9c803ac36a64
  - Body: Day view dark mode is now in beta.
  - Reason: Status update from 2026-10-16 notes.

- Decision - Concierge onboarding is live; onboarding rollout is complete; day view dark mode in beta
  - ID: 4fa51a32-de76-4d3f-ad78-3522cb275e95
  - Body: Concierge onboarding is live for pilot clinics; onboarding rollout completed; day view dark mode is in beta.
  - Reason: Status update from 2026-10-15 notes.
  - Supersedes: Onboarding policy in older decision (see below).

- Decision - Move analytics to PostHog Cloud (EU region)
  - ID: cd60f4c9-9c11-4e0a-90c0-b4a9a91aba6b
  - Body: Switch analytics to PostHog Cloud hosted in the EU region to keep clinic data within EU. Stop self-hosted/PostHog on-prem.
  - Reason: Tom & Maya decision around 2026-10-14.

- Decision - Investor update cadence is fortnightly update with a metrics dashboard link
  - ID: 4c978259-4b49-4a2a-bccc-e4122150c649
  - Body: Investor updates cadence changed to fortnightly with a metrics dashboard link; replaces monthly cadence.
  - Reason: Align with 2026-10-16 notes.
  - Supersedes: Decision - Investor update cadence is monthly (see below).

- Note on superseding relations
  - Superseded Tailwind UI kit decision: new Tailwind→shadcn/ui decision links to old Tailwind decision (via manage_links.add). Source: eebb4b47 supersedes 02437649-4835-4d9d-8576-917b980e8b66.
  - Superseded PostHog self-hosted: PostHog EU decision (cd60f4c9) supersedes f004a28a-0f5b-4147-9470-c5e335b1e803.
  - Superseded investor cadence monthly: Fortnightly decision (4c978259) supersedes 0d9d5ca0-fe2e-4b79-9d18-78663ef2bba5.

Decisions superseding old onboarding policy
- Superseded onboarding policy
  - Source: 4fa51a32-de76-4d3f-ad78-3522cb275e95 supersedes the onboarding policy in 1cef8ddb-a093-40c7-929d-4f0a854b6c4c.

New tasks created
- Task - Redesign SMS reminder templates for Sinch
  - ID: a62574bf-38e1-4034-abbb-594b7987e676
  - Body: Redesign the SMS reminder templates to align with Sinch, including message copy, fallback flows, and error handling. Due by 30 October 2026.
  - Reason: Priya redesigns per 13 Oct notes.

- Task - Investigate per-practitioner colours on the calendar
  - ID: ee8dd32a-651e-4980-b0fa-ff2c2182d5b7
  - Body: Prototype calendar view options with per-practitioner color coding and gather feedback from receptionists.
  - Reason: Receptionists requested per-practitioner colors.

- Task - Evaluate Plain pricing vs Zendesk; revisit in December
  - ID: d32fc160-2b1f-400e-962c-fa9ae9fd76d5
  - Body: Compare Plain and Zendesk pricing and capabilities; revisit decision in December.
  - Reason: Not decided in 13 Oct notes; plan to revisit.

Task updates and completions
- Task - Roll out sms reminder provider (Vonage)
  - ID: 07a1c90f-73a3-4e80-a603-6754719863bc
  - Status updated to closed
  - Reason: Replaced by decision Move SMS reminders to Sinch; Vonage rollout is no longer needed.

Other notes reflected
- I added a Day view dark mode in beta decision (b7477f7c) to acknowledge the note that dark mode for the day view is in beta.

What I did not delete
- I did not delete any existing records; I created new decisions/tasks and updated statuses as per what was agreed or observed in the notes. I also added supersedes links to indicate replacements where applicable.

Short summary of changes
- Added four major decisions:
  - Move SMS reminders to Sinch (replacing Vonage)
  - Replace Tailwind UI kit with shadcn/ui
  - Move analytics to PostHog Cloud EU
  - Fortnightly investor updates with a metrics dashboard link (superseding monthly cadence)
  - Concierge onboarding live; onboarding rollout complete
  - Day view dark mode in beta
- Updated onboarding decision to reflect live status and superseded older onboarding policy
- Superseded older related decisions with links to new ones
  - Tailwind UI kit → shadcn/ui
  - PostHog self-hosted → PostHog Cloud EU
  - Investor cadence monthly → fortnightly
  - Onboarding flow policy superseded by concierge onboarding live status
- Closed the Vonage SMS rollout task (07a1c90f...), replacing it with the Sinch plan
- Created new tasks for Priya (SMS redesign), per-practitioner calendar colors, and Plain vs Zendesk pricing with December revisit
- All actions preserve historical records; nothing deleted.