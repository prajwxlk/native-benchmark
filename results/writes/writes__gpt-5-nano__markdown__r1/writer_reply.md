I updated Fernwork’s vault to reflect the week of 13 October 2026, recording new decisions, updating task statuses, and adding new tasks. Summary of changes:

What I added
- New weekly sync note
  - vault/Fernwork HQ/Meetings/Weekly sync 2026-10-13.md
  - Contains Attendees, Decisions (6 items: SMS Sinch, Onboarding rollout, PostHog Cloud EU, Release cadence, Investor updates, Design system), and Actions (design SMS templates, Vonage decommissioning, analytics migration, release cadence monitoring, calendar color backlog).

- New decision notes (replacing older ones)
  - vault/Fernwork HQ/Decisions/Decision - SMS reminder provider is Sinch.md
  - vault/Fernwork HQ/Decisions/Decision - Onboarding rollout is live.md
  - vault/Fernwork HQ/Decisions/Decision - Product analytics vendor is PostHog Cloud (EU region).md
  - vault/Fernwork HQ/Decisions/Decision - Release cadence is twice-weekly releases on Tuesdays and Thursdays.md
  - vault/Fernwork HQ/Decisions/Decision - Investor update cadence is monthly update.md
  - vault/Fernwork HQ/Decisions/Decision - Design system is shadcn/ui.md

  - Each new decision:
    - Sets date to 2026-10-13 and status to decided.
    - Lists decided_by (Maya Okafor for most, Tom Lindqvist for release cadence, Kenji Watanabe for onboarding rollout).
    - Replaces the prior decision (with a replaces field pointing to the old decision file).
    - Provides rationale and notes on why the change was made.

- Updated and added tasks
  - Updated existing task:
    - vault/Fernwork HQ/Work/Tasks/Task - Roll out sms reminder provider (Vonage).md
      - status changed from in_progress to cancelled
      - Implements updated to new decision: Sinch
      - Added note that this task is superseded by the new Move SMS reminders task
  - New task:
    - vault/Fernwork HQ/Work/Tasks/Task - Move SMS reminders to Sinch (from Vonage).md
      - status: open
      - owner: Kenji Watanabe
      - implements: Decision - SMS reminder provider is Sinch
      - Done when: migration live; Sinch active; Vonage decommissioned
      - Contains planned steps and notes

What I changed (highlights)
- Replaced an old decision with updated ones and linked replacements:
  - SMS reminder provider: Vonage -> Sinch
  - Onboarding flow decision replaced by Onboarding rollout being live
  - Product analytics: PostHog self-hosted -> PostHog Cloud (EU)
  - Release cadence: weekly Thursday -> twice-weekly Tue/Thu
  - Investor updates: fortnightly -> monthly
  - Design system: Tailwind UI kit -> shadcn/ui
- Updated the Roll out sms reminder task to reflect cancellation and linked it to the new Move SMS reminders task.

What I did not remove
- I did not delete any existing notes or decisions; I only added new ones and marked the old ones as replaced where applicable, per your instruction.

If you’d like, I can add due dates or owners to more tasks, or create additional cross-links between related decisions and tasks.