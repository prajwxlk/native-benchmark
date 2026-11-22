I’ve updated the workspace to reflect the week of 13 October 2026.

What I changed
- Added a new Fernwork inbox note: vault/fernwork_inbox_2026_10_13.md
  - Records key decisions and their replacements where applicable.
  - Updates task statuses and adds new tasks based on the meeting notes.
  - Uses YAML frontmatter and [[wikilinks]] as per existing conventions.

Key decisions and replacements recorded
- SMS reminders
  - Decision: Move SMS reminders from Vonage to Sinch, effective 2026-11-01.
  - Replacement: Replaces the prior decision to continue using Vonage for SMS reminders.
  - Vonage rollout: Note that Kenji’s Vonage rollout task is now unnecessary.
- Analytics hosting
  - Decision: Switch from self-hosted PostHog to PostHog Cloud (EU region) to keep clinic data in the EU.
  - Replacement: Replaces the earlier stance of self-hosting PostHog.
- Design system
  - Decision: Replace Tailwind UI kit with shadcn/ui as the design system.
  - Replacement: Replaces the previous Tailwind UI kit usage.
- Onboarding and day view
  - Decision: Concierge onboarding is live for all pilot clinics; onboarding rollout task is done (status: Completed).
  - Decision: Dark mode for the day view is in beta (status: In beta).
- Investor updates
  - Decision: Investor updates go back to monthly, but keep the metrics dashboard link (status: Active policy).

New and updated tasks (with status)
- Priya to redesign the SMS reminder templates for Sinch by 2026-10-30. Status: In progress.
- Investigate per-practitioner colours on the calendar. Status: Open.
- Revisit the support tool decision (Plain vs Zendesk) in December. Status: Planned for December.
- Implement PostHog Cloud EU region for analytics. Status: Implemented.
- Implement twice-weekly releases cadence (Tuesday/Thursday) behind feature flags. Status: In effect.
- Replace Tailwind UI kit with shadcn/ui in the design system. Status: Completed.
- Onboarding rollout completed for concierge; dark mode day view in beta. Status: Completed (onboarding) / Beta (dark mode).

Notes
- I did not delete any existing notes; I only added new entries and updated task/decision statuses as reflected above.
- The new note links to related topics via [[PostHog Cloud EU]], [[Deployment schedule]], [[Metrics dashboard]], and [[Design system]] for context.

If you want me to adjust formats, add more links, or create separate pages for each decision (with explicit “replaces” references), I can expand accordingly.