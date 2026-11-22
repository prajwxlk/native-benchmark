Here’s what I updated in Fernwork’s Native workspace based on the week of 2026-10-13 notes:

New decisions (Resolution records)
- PostHog analytics moved to Cloud EU
  - ID: 2d4a62ca-4578-4ac0-bede-c83527ff8c6a
  - Name: Switch product analytics to PostHog Cloud (EU region)
  - Summary: Move from self-hosted PostHog to PostHog Cloud in the EU; aligns with data staying in EU and reduces ops time.
  - Supersedes: f004a28a-0f5b-4147-9470-c5e335b1e803 (PostHog self-hosted decision)

- SMS reminders moved to Sinch; Vonage decommissioned
  - ID: 300bc489-23bc-474d-8e31-8b106d8fdd9e
  - Name: Move SMS reminders to Sinch; decommission Vonage
  - Summary: Migrating SMS reminders to Sinch effective 1 November; Vonage rollout stopped.
  - Supersedes: 28e16715-b34d-4570-95dd-b363bd47fd5a (Decision: SMS reminder provider is Vonage)

- Twice-weekly releases behind feature flags
  - ID: 916e9dcc-c951-4a4d-8811-f52192f94b7d
  - Name: Ship releases twice-weekly on Tuesdays and Thursdays behind feature flags
  - Summary: Adopt 2 releases per week, Tue/Thu, behind feature flags.
  - Supersedes: 316a7a96-e0ed-4bf4-8523-40eacd52e8a9 (Decision: continuous deploys behind feature flags)

- Investor updates cadence: monthly
  - ID: c92d1c3d-be48-4dbf-9893-6593fb94a6e6
  - Name: Investor updates cadence changed to monthly; keep metrics dashboard link
  - Summary: Investor updates moved to monthly cadence; maintain metrics dashboard link.
  - Supersedes: 0d9d5ca0-fe2e-4b79-9d18-78663ef2bba5 (Investors cadence decision)

- Design system change: Tailwind UI kit to shadcn/ui
  - ID: b536efc9-25b8-4d87-a8e4-83d484c1eb3a
  - Name: Replace Tailwind UI kit with shadcn/ui as design system
  - Summary: Adopt shadcn/ui as the new design system, replacing Tailwind UI kit.
  - Supersedes: 02437649-4835-4d9d-8576-917b980e8b66 (Decision: Design system is Tailwind UI kit)

New tasks (WorkItem records)
- SMS reminders: redesign templates for Sinch
  - ID: 602bca78-5386-4d7a-9b6e-b963f46d8e8f
  - Lifecycle: open
  - Due: 2026-10-30
  - Body: Redesign SMS reminder templates for Sinch; due 2026-10-30.
  - Reason: Action item from 2026-10-13 weekly sync.

- Concierge onboarding rollout completed
  - ID: 714985c9-3d1f-4522-bc34-66073da4b910
  - Lifecycle: completed
  - Body: Concierge onboarding is live for all pilot clinics; onboarding rollout task is completed.
  - Summary added later: “Onboarding rollout completed: Concierge onboarding live for all pilot clinics; help center updated.”

- Dark mode day view: beta
  - ID: 11f1291c-7427-4dc6-9613-cc2f7d3fac66
  - Lifecycle: open
  - Body: Dark mode for day view is now in beta; monitor feedback and plan next steps.

- Vonage rollout stopped
  - ID: 050d9c87-1c07-4617-9258-e7174262e550
  - Lifecycle: open
  - Body: Vonage SMS rollout stopped; Sinch will handle SMS reminders going forward.

Status updates and notes (task state changes)
- Onboarding rollout completed
  - Updated record: 714985c9-3d1f-4522-bc34-66073da4b910
  - Status: completed
  - Summary added: “Onboarding rollout completed: Concierge onboarding live for all pilot clinics; help center updated.”

- Supersedes relationships added
  - PostHog: 2d4a62ca supersedes f004a28a
  - SMS reminders: 300bc489 supersedes 28e16715
  - Release cadence: 916e9dcc supersedes 316a7a96
  - Investor cadence: c92d1c3d supersedes 0d9d5ca0
  - Design system: b536efc9 supersedes 02437649

What I did not record
- No decision or task was created for items explicitly “not decided” in the notes (e.g., re: Plain vs Zendesk pricing) without a concrete agreement or task.
- I did not delete any records; I only added decisions, tasks, and supersedes relationships, and updated the onboarding task status.

If you want, I can add due dates or owners to the new tasks, or create additional supersedes for earlier related decisions.