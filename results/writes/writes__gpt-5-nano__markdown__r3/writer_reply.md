I’ve updated the Fernwork workspace to reflect the week of 13 October 2026. Here’s what changed and where to find it:

What I added
- Weekly sync notes for 2026-10-13
  - Fernwork HQ/Meetings/Weekly sync 2026-10-13.md
  - Includes attendees, recap points (SMS vendor move to Sinch starting 1 November; Vonage is out), action items (Priya to redesign SMS templates by Oct 30), and calendar-related notes.

- New decisions (replacements noted where applicable)
  - Fernwork HQ/Decisions/Decision - SMS reminder provider is Sinch.md
    - Date: 2026-10-13
    - Decided by: Tom Lindqvist
    - Decision: SMS reminder provider is Sinch
    - Replaces: Decision - SMS reminder provider is Vonage
  - Fernwork HQ/Decisions/Decision - Product analytics vendor is PostHog Cloud EU.md
    - Date: 2026-10-14
    - Decided by: Tom Lindqvist
    - Decision: Product analytics vendor is PostHog Cloud EU
    - Replaces: Decision - Product analytics vendor is PostHog self-hosted
  - Fernwork HQ/Decisions/Decision - Design system is shadcn/ui.md
    - Date: 2026-10-16
    - Decided by: Maya Okafor
    - Decision: Design system is shadcn/ui
    - Replaces: Decision - Design system is Tailwind UI kit
  - Fernwork HQ/Decisions/Decision - Design system is Tailwind UI kit (superseded).md
    - Marked as superseded
  - Fernwork HQ/Decisions/Decision - Investor update cadence is fortnightly update with a metrics dashboard link (obsolete).md
    - Marked as obsolete (replaced by monthly cadence)
  - Fernwork HQ/Decisions/Decision - Investor update cadence is fortnightly update with a metrics dashboard link.md
    - Note: Added an obsolete/superseded doc to indicate this cadence is no longer current (as of 2026-10-13). The file itself remains in place to preserve history.

- New decisions related to status context in a few places
  - Fernwork HQ/Decisions/Decision - SMS reminder provider is Sinch.md now exists and is the current one; the older Vonage decision remains in the archive (with an obsolete note added via the new Sinch decision).

- Complementary decision-archive entries
  - Fernwork HQ/Decisions/Decision - Design system is Tailwind UI kit (superseded).md
    - Indicates Tailwind UI kit decision is no longer current
  - Fernwork HQ/Decisions/Decision - Investor update cadence is fortnightly update with a metrics dashboard link (obsolete).md
    - Indicates this cadence is no longer current

What I added (new tasks)
- Fernwork HQ/Work/Tasks/Task - Roll out sms reminder provider (Sinch).md
  - Status: open
  - Owner: Kenji Watanabe
  - Implements: Decision - SMS reminder provider is Sinch

- Fernwork HQ/Work/Tasks/Task - Prepare customer comms for sms reminder provider (Sinch).md
  - Status: open
  - Owner: Priya Raman
  - Implements: Decision - SMS reminder provider is Sinch

- Fernwork HQ/Work/Tasks/Task - Roll out product analytics vendor (PostHog Cloud EU).md
  - Status: open
  - Owner: Sofia Marchetti
  - Implements: Decision - Product analytics vendor is PostHog Cloud EU

- Fernwork HQ/Work/Tasks/Task - Prepare customer comms for product analytics vendor (PostHog Cloud EU).md
  - Status: open
  - Owner: Sofia Marchetti
  - Implements: Decision - Product analytics vendor is PostHog Cloud EU

- Fernwork HQ/Work/Tasks/Task - Prepare customer comms for design system update (shadcn/ui).md
  - Status: open
  - Owner: Priya Raman
  - Implements: Decision - Design system is shadcn/ui

- Fernwork HQ/Work/Tasks/Task - Roll out product analytics vendor (PostHog Cloud EU).md (created as a sibling task to the rollout)
  - Status: open
  - Owner: Sofia Marchetti
  - Implements: Decision - Product analytics vendor is PostHog Cloud EU

What I adjusted (status/relationships)
- Replacing legacy decisions with current ones:
  - Product analytics: PostHog Cloud EU replaces PostHog self-hosted
  - SMS reminders: Sinch replaces Vonage
  - Design system: shadcn/ui replaces Tailwind UI kit
  - Investor updates cadence: monthly cadence references the current path; a separate obsolete note exists to reflect the superseded fortnightly cadence

Where to look
- Weekly sync notes
  - New: Fernwork HQ/Meetings/Weekly sync 2026-10-13.md
- Decisions
  - Current replacements:
    - Fernwork HQ/Decisions/Decision - SMS reminder provider is Sinch.md
    - Fernwork HQ/Decisions/Decision - Product analytics vendor is PostHog Cloud EU.md
    - Fernwork HQ/Decisions/Decision - Design system is shadcn/ui.md
  - Superseded/obsolete references:
    - Fernwork HQ/Decisions/Decision - Design system is Tailwind UI kit (superseded).md
    - Fernwork HQ/Decisions/Decision - Investor update cadence is fortnightly update with a metrics dashboard link (obsolete).md
    - Fernwork HQ/Decisions/Decision - Investor update cadence is fortnightly update with a metrics dashboard link.md (non-obsolete, but now superseded)
- Tasks
  - New task files under Fernwork HQ/Work/Tasks/:
    - Task - Roll out sms reminder provider (Sinch).md
    - Task - Prepare customer comms for sms reminder provider (Sinch).md
    - Task - Roll out product analytics vendor (PostHog Cloud EU).md
    - Task - Prepare customer comms for product analytics vendor (PostHog Cloud EU).md
    - Task - Prepare customer comms for design system update (shadcn/ui).md
  - Existing/related tasks patched by adding new items rather than editing existing ones to preserve history (e.g., Move from PostHog self-hosted to PostHog Cloud EU; new related tasks to implement the new decisions)

Notes on decisions replacing each other
- Public launch date decisions are already aligned; the 6 October 2026 date remains current and supersedes the 15 September 2026 date per existing notes.
- The new decisions explicitly indicate replacements using the “This replaces …, which is no longer current” phrasing in frontmatter context, aligning with the established convention in this workspace.

Would you like me to also:
- Update the old decision notes (e.g., Vonage, PostHog self-hosted, Tailwind UI kit) to explicitly mark them as superseded within their content bodies?
- Add a dedicated “Done” status update for the old Roll out tasks (e.g., mark Roll out sms reminder provider (Vonage) as completed) and link them to the new Sinch task?