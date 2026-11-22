Here’s what I updated in Fernwork’s Native workspace (week of 2026-10-13 notes):

Decisions created (Resolution/decision)
- Move SMS reminders to Sinch; Vonage decommissioned
  - ID: 33bdc208-fff8-440d-8b76-9715dfcbc3e2
  - Short reference: 33bdc20
  - Summary: Move SMS reminders from Vonage to Sinch starting 1 November 2026; Vonage rollout is being stopped.
  - Reason: Vonage failures on Portuguese numbers; action to move to Sinch.

- Switch analytics to PostHog Cloud (EU region)
  - ID: 2b3c97b0-d0e5-475d-b794-16eaa9f7e7b2
  - Short reference: 2b3c97b
  - Summary: Switch product analytics from self-hosted PostHog to PostHog Cloud in the EU region to keep data in EU and reduce ops.
  - Reason: Self-hosting was time-consuming; EU cloud preferred.

- Ship twice-weekly releases on Tuesdays and Thursdays behind feature flags
  - ID: b5907b61-59b6-48d5-ba68-56c18e5916c2
  - Short reference: b5907b6
  - Summary: Implement a twice-weekly release cadence, still behind feature flags.
  - Reason: Daniel Reyes (2026-10-15) decision.

- Concierge onboarding rollout completed
  - ID: 05a7a80a-9ba9-420b-970b-73084601e9f9
  - Short reference: 05a7a80
  - Summary: Concierge onboarding is live for all pilot clinics and the help centre is updated; onboarding rollout task is done.
  - Reason: Kenji’s note (2026-10-15).

- Dark mode day view beta
  - ID: 31be270c-ff34-4a75-963f-c27f1730e1c2
  - Short reference: 31be270
  - Summary: Dark mode for the day view is in beta.
  - Reason: Maya/Kenji notes (2026-10-16).

- Replace Tailwind UI kit with shadcn/ui as design system
  - ID: 0c0e9e55-5a0d-4f38-bc51-32f5236f1a0f
  - Short reference: 0c0e9e5
  - Summary: Design system switch from Tailwind UI kit to shadcn/ui.
  - Reason: Agreement between Maya and Priya (2026-10-16).

- Investor update cadence: monthly
  - ID: ea95e54c-68cd-40f0-8939-e08dbe34a764
  - Short reference: ea95e54
  - Summary: Investor updates return to monthly cadence with a metrics dashboard link.
  - Reason: Brightpath requested monthly cadence (2026-10-16).

- Supersession notes (linkages to show current state)
  - Move SMS reminders to Sinch supersedes older SMS reminder decision (Vonage)
    - Link: 33bdc208 supersedes 28e16715 (Vonage-based SMS reminder decision)
  - Investor update cadence: monthly supersedes fortnightly cadence
    - Link: ea95e54 supersedes 4c97825 (fortnightly cadence with metrics dashboard)
      - Found record: 4c978259-4b49-4a2a-bccc-e4122150c649 (Decision - Investor update cadence is fortnightly update with a metrics dashboard link)

Tasks created
- Redesign SMS reminder templates for Sinch
  - ID: f8cb98fd-f178-45ee-a3ae-dfed7246224d
  - Lifecyle: open
  - Summary: Redesign SMS reminder templates for Sinch; due by 30 October 2026.
  - Reason: Action from 2026-10-13 weekly sync (Priya to redesign by Oct 30).

- Onboarding rollout for concierge onboarding (pilot clinics) completed
  - ID: 8bd179f1-e37f-4fa9-82a0-be0419f40dbf
  - Lifecyle: open
  - Summary: Onboarding rollout completed for concierge onboarding; pilot clinics live; help center updated.
  - Reason: Kenji note (2026-10-15).

- Test and refine dark mode day view (beta)
  - ID: eb03e168-9821-4b6e-97cf-2014bfa99d41
  - Lifecyle: open
  - Summary: Test/refine the dark mode for day view in beta; collect feedback.
  - Reason: Reflects Dark mode day view beta decision.

- Rollout status update: Roll out onboarding flow (concierge onboarding call before account creation)
  - ID: 63677d9c-ecba-4056-94a0-b49caeee4fd6
  - Lifecyle: completed
  - Summary: Roll out onboarding flow completed; live for all pilots; notes updated.
  - Reason: Task previously in progress; now completed and summary added.

Updated existing tasks
- Roll out onboarding flow (concierge onboarding call before account creation)
  - ID: 63677d9c-ecba-4056-94a0-b49caeee4fd6
  - Status updated to completed
  - Summary added: “Onboarding rollout live for all pilot clinics; help center updated.”
  - Reason: Rollout completed as per 2026-10-15 notes.

Notes on replacements and scope
- New decisions were created for the major shifts in SMS reminders, analytics hosting, release cadence, onboarding, visual theming, and investor cadence. Where an older decision existed on the same topic, I added supersedes links to indicate the newer current decision:
  - 33bdc208 supersedes 28e16715 (Vonage SMS reminder decision)
  - ea95e54c supersedes 4c97825 (Fortnightly investor cadence)

- I did not delete any prior records. I only added new decisions/tasks and linked superseding decisions where applicable.

If you want, I can export a compact changelog or prune any older entries that are now superseded but still in the archive.