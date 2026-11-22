I updated Fernwork’s Native workspace to reflect the 13–16 Oct 2026 notes. Summary of changes:

New decisions recorded
- Move SMS reminders to Sinch
  - ID: 2d6e0c58-6b03-41bf-b2fb-26687e30a383
  - Details: Migrate SMS reminders from Vonage to Sinch starting 1 Nov 2026; Vonage decommissioned.
  - Replaces: SMS reminder provider is Vonage (ID: 28e1671)
  - Relationship added: supersedes
- Switch product analytics to PostHog Cloud (EU region)
  - ID: b2798668-8d12-41cc-9c2d-39fd50fb05b8
  - Details: Move from PostHog self-hosted to PostHog Cloud in EU region.
  - Replaces: Product analytics vendor is PostHog self-hosted (ID: f004a28a)
  - Relationship added: supersedes
- Ship twice-weekly releases on Tuesdays and Thursdays behind feature flags
  - ID: f20c948d-e642-4f6c-bfa9-08f63c76b09a
  - Details: Cadence: twice-weekly releases, behind feature flags.
- Replace Tailwind UI kit with shadcn/ui as design system
  - ID: 15ac18e8-3433-4125-9581-2b4df04e7ff5
  - Details: Design system switch to shadcn/ui.
- Investor updates cadence: monthly with metrics dashboard link
  - ID: 691377dd-1131-4461-a36b-1b7f41413dab
  - Details: Slow cadence back to monthly; keep metrics dashboard link.
  - Replaces: Investor update cadence is fortnightly update with a metrics dashboard link (ID: 4c97825)
  - Relationship added: supersedes

Link updates (replacing older decisions)
- Superseded the old Vonage decision
  - Link: Move SMS reminders to Sinch (2d6e0c58) -> SMS reminder provider is Vonage (28e1671)
- Superseded the old PostHog self-hosted decision
  - Link: Switch product analytics to PostHog Cloud (EU region) (b2798668) -> Product analytics vendor is PostHog self-hosted (f004a28a)
- Superseded the fortnightly investor cadence
  - Link: Investor updates cadence monthly (691377dd) -> Investor update cadence is fortnightly update with a metrics dashboard link (4c97825)

Task updates
- Roll out sms reminder provider (Vonage)
  - Updated: closed
  - Reason: Replaced by Sinch migration; new decision supersedes Vonage rollout.
  - Old ID: 07a1c90
- Roll out product analytics vendor (PostHog self-hosted)
  - Updated: closed
  - Reason: Replaced by PostHog Cloud EU decision.
  - Old ID: 0b49dca3
- Update billing and docs for product analytics vendor (PostHog self-hosted)
  - Updated: closed
  - Reason: Replaced by PostHog Cloud EU decision.
  - Old ID: e0375d57
- Redesign SMS reminder templates for Sinch
  - New task
  - ID: 22a5d706-0109-4374-b2cd-cc1667a34341
  - Lifecycle: open
  - Body notes due date (30 Oct 2026)
- Onboarding rollout completed for concierge onboarding
  - New task
  - ID: 987c6734-b0a3-4dd6-ae66-9756ca9b6387
  - Lifecycle: completed
  - Summary added: Onboarding rollout completed; concierge onboarding live; help center updated; dark mode for day view in beta.

New completed status noted
- Onboarding rollout completed (987c6734-...), with a summary describing what was achieved.

What I did not delete
- I did not delete any records. I created new decisions and tasks, and updated statuses and supersedence links for traceability.

If you want, I can export a compact changelog or generate a quick dashboard view of current decision cadence and supersedes.