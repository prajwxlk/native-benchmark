I updated Fernwork’s Native workspace to reflect the week of 2026-10-13 notes. Summary of changes:

New decisions (Resolution, designations reflect what was agreed)
- Move SMS reminders from Vonage to Sinch starting 1 November
  - ID: 21c94915-34d3-4570-be7a-616f3d22eec1
  - Reason: SMS move due to Vonage issues; Sinch to handle reminders
  - Supersedes: Vonage SMS reminder decision (ID: 28e16715-b34d-4570-95dd-b363bd47fd5a)
  - Link added: source 21c94915 -> target 28e16715 with relationship "supersedes"
- Decision - Product analytics vendor is PostHog Cloud (EU region)
  - ID: 86586b94-3f1b-4425-b703-d0636eeb94c8
  - Reason: Self-hosted analytics replaced with PostHog Cloud in EU
  - Supersedes: PostHog self-hosted decision (ID: f004a28a-0f5b-4147-9470-c5e335b1e803)
  - Link added: source 86586b94 -> target f004a28a with relationship "supersedes"
- Concierge onboarding rollout completed
  - ID: 75384259-7d50-4a4b-86e2-84a8bdfb5035
  - Reason: Onboarding live for all pilot clinics; help centre updated; onboarding rollout task done
- Design system is shadcn/ui
  - ID: 68c54ab2-0a67-43f0-a927-324f885a2f5b
  - Reason: Replaced Tailwind UI kit with shadcn/ui
  - Supersedes: Tailwind UI kit design decision (ID: 02437649-4835-4d9d-8576-917b980e8b66)
  - Link added: source 68c54ab2 -> target 02437649 with relationship "supersedes"
- Redesign SMS reminder templates for Sinch
  - ID: 5fa5308a-8d6a-487c-9d45-87966373dfb4
  - Reason: Priya to redesign SMS templates for Sinch; due by 30 Oct

New tasks (WorkItem, open by default)
- Redesign SMS reminder templates for Sinch
  - ID: 5fa5308a-8d6a-487c-9d45-87966373dfb4
  - Due: 30 October
- Investigate per-practitioner colours on the calendar
  - ID: 50d06b15-e937-4401-b9f6-115e42e74d5f
- Revisit support tool Plain vs Zendesk in December
  - ID: da9bb831-bee4-4138-89b6-256dffd9cd5e
- Ship twice-weekly releases on Tuesdays and Thursdays, behind feature flags
  - ID: 78b6da5e-fec7-4b95-8bd3-2406715606e7

Status updates (recorded)
- PostHog self-hosted rollout task updated to closed (since we’re switching to PostHog Cloud EU)
  - Task: Roll out product analytics vendor (PostHog self-hosted)
  - ID: 0b49dca3-00e9-4428-9142-549797d37fab
  - Lifecycle: closed
  - Reason: Replaced by PostHog Cloud EU decision
- Concierge onboarding rollout task updated to completed
  - Task: Roll out onboarding flow (concierge onboarding call before account creation)
  - ID: 63677d9c-ecba-4056-94a0-b49caeee4fd6
  - Lifecycle: completed
  - Summary added: Onboarding rollout completed; concierge onboarding live; help centre updated
  - Note: Summary added to address completion outcome

Notes on not deleting anything
- All items added are recorded as new or updated; no deletions were performed.
- Replacements are recorded via supersedes links so readers can trace current vs. prior decisions.

What’s next
- Confirm ownership and due dates for the new tasks (especially the Sinch SMS templates due by Oct 30 and the per-practitioner calendar colors work).
- If you want, I can add owners or assign specific assignees to each new task.
- I can also pull a quick view of all current decisions and supersedes to surface the latest design/system, analytics, and cadence decisions.

Short summary of changes completed
- Added 5 new decisions (Move SMS to Sinch; PostHog Cloud EU; Concierge onboarding completed; Design system shadcn/ui; Redesign SMS templates for Sinch).
- Created 4 new tasks (Redesign SMS templates; Investigate per-practitioner colours; Revisit Plain vs Zendesk; Ship twice-weekly releases).
- Updated statuses for existing work (closed PostHog self-hosted rollout; completed concierge onboarding rollout task).
- Established supersedes links to reflect replacements (Tailwind UI kit → shadcn/ui; Vonage → Sinch for SMS reminders; PostHog self-hosted → PostHog Cloud EU).