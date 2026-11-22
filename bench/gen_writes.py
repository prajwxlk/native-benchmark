"""Generate the write benchmark: a week of new messages, and the end state they imply.

Outputs (under data/writes/):
  feed.md          what the agent is asked to file: one sync plus five messages, 13-16 Oct 2026
  scenarios.json   expected end state, checked by bench/run_writes.py
  readback.json    questions a fresh reader answers afterwards against the updated workspace

The feed mixes real changes (five decisions replaced, one task finished, one task made
pointless, one new task) with distractors (a proposal nobody agreed to, and a fact that is
already recorded). Every scenario is resolved against data/truth.json, so it breaks loudly
if the corpus changes.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "writes"

# Words that, in an edited old note or a new note, say "this one is no longer current".
STALE_MARKERS = r"supersed|replaced|no longer current|outdated|obsolete|deprecated"


def main():
    truth = json.loads((DATA / "truth.json").read_text())
    th = truth["threads"]

    def current(topic):
        return th[topic]["current"]

    def task(title):
        assert title in truth["tasks"], title
        return title

    replace = [
        {"id": "R1", "topic": "sms provider", "old": current("sms provider"), "old_value": "Vonage",
         "new_value": "Sinch", "keys": [["Sinch"]]},
        {"id": "R2", "topic": "analytics", "old": current("analytics"), "old_value": "PostHog self-hosted",
         "new_value": "PostHog Cloud (EU region)", "keys": [["PostHog", "Cloud"]]},
        {"id": "R3", "topic": "release cadence", "old": current("release cadence"),
         "old_value": "continuous deploys", "new_value": "twice-weekly releases on Tuesdays and Thursdays",
         "keys": [["Tuesday"], ["twice-weekly"], ["twice a week"]]},
        {"id": "R4", "topic": "investor updates", "old": current("investor updates"),
         "old_value": "fortnightly", "new_value": "monthly update with a metrics dashboard link",
         "keys": [["monthly", "dashboard"]]},
        {"id": "R5", "topic": "design system", "old": current("design system"), "old_value": "Tailwind UI kit",
         "new_value": "shadcn/ui", "keys": [["shadcn"]]},
    ]
    for r in replace:
        assert truth["decisions"][r["old"]]["value"].startswith(r["old_value"].split()[0]), r
    tasks = [
        {"id": "T1", "title": task("Task - Roll out onboarding flow (concierge onboarding call before account creation)"),
         "before": "in_progress", "accept": ["completed", "done", "complete"]},
        {"id": "T2", "title": task("Task - Roll out sms reminder provider (Vonage)"), "before": "in_progress",
         "accept": ["closed", "cancelled", "canceled", "obsolete", "abandoned", "dropped", "wontfix", "won't do"]},
    ]
    new_tasks = [{"id": "T3", "name_keys": [["template"]], "owner": "Priya"}]
    distractors = [
        {"id": "D1", "topic": "support tool", "current": current("support tool"), "forbid_keys": [["Zendesk"]],
         "why": "Zendesk was only proposed; Plain stays current"},
        {"id": "D2", "topic": "launch date", "current": current("launch date"), "forbid_keys": [["launch"]],
         "why": "the launch date is already recorded; no new decision"},
    ]
    for t in tasks:
        assert truth["tasks"][t["title"]]["status"] == t["before"], t

    feed = f"""# Fernwork inbox, week of 13 October 2026

## Weekly sync, 2026-10-13
Attendees: Maya Okafor, Tom Lindqvist, Priya Raman, Daniel Reyes, Sofia Marchetti, Kenji Watanabe

- Launch recap: we launched publicly on 6 October as planned. Early feedback from clinics is good.
- SMS reminders: Vonage keeps failing on Portuguese numbers too. Agreed: we move SMS reminders to Sinch from 1 November. Vonage is out.
- Kenji to stop the Vonage rollout; that task is no longer needed.
- Action: Priya to redesign the SMS reminder templates for Sinch by 30 October.
- Support tool: Sofia floated moving from Plain to Zendesk. Not decided; Maya wants to see Plain's new pricing first. Revisit in December.
- Several receptionists asked again for per-practitioner colours on the calendar.

## Message from Tom Lindqvist, 2026-10-14
Self-hosting PostHog is eating too much ops time. Maya and I agreed we switch product analytics to PostHog Cloud (EU region), so clinic data still stays in the EU.

## Message from Daniel Reyes, 2026-10-15
Continuous deploys keep surprising pilot clinics in the middle of the day. Decided with Tom: from now on we ship twice-weekly releases on Tuesdays and Thursdays, still behind feature flags.

## Message from Kenji Watanabe, 2026-10-15
Concierge onboarding is live for all pilot clinics and the help centre is updated, so the onboarding rollout task is done. Also, dark mode for the day view is now in beta.

## Message from Maya Okafor, 2026-10-16
Brightpath asked us to slow down: investor updates go back to monthly, but we keep the metrics dashboard link.
Separately, Priya and Kenji agreed we replace the Tailwind UI kit with shadcn/ui as our design system.
"""
    readback = [
        {"id": "Q1", "question": "What SMS reminder provider are we using or moving to now?", "keys": [["Sinch"]], "for": "R1"},
        {"id": "Q2", "question": "What is our product analytics vendor now?", "keys": [["Cloud"]], "for": "R2"},
        {"id": "Q3", "question": "What is our release cadence now?", "keys": [["Tuesday"], ["twice"]], "for": "R3"},
        {"id": "Q4", "question": "What is our investor update cadence now?", "keys": [["monthly", "dashboard"]], "for": "R4"},
        {"id": "Q5", "question": "What design system do we use now?", "keys": [["shadcn"]], "for": "R5"},
        {"id": "Q6", "question": "What customer support tool do we use now?", "keys": [["Plain"]], "for": "D1"},
        {"id": "Q7", "question": f"What is the status of the task '{tasks[0]['title']}'? "
                                 "Answer with its status word (for example open, in_progress, completed or closed).",
         "keys": [["complete"], ["done"]], "for": "T1"},
        {"id": "Q8", "question": f"What is the status of the task '{tasks[1]['title']}'? "
                                 "Answer with its status word (for example open, in_progress, completed or closed).",
         "keys": [[w] for w in ("closed", "cancel", "obsolete", "abandon", "dropped", "no longer needed", "stopped")],
         "for": "T2"},
        {"id": "Q9", "question": "Who owns the task to redesign the SMS reminder templates?", "keys": [["Priya"]], "for": "T3"},
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "feed.md").write_text(feed)
    (OUT / "scenarios.json").write_text(json.dumps(
        {"replace": replace, "tasks": tasks, "new_tasks": new_tasks, "distractors": distractors,
         "stale_markers": STALE_MARKERS}, indent=2))
    (OUT / "readback.json").write_text(json.dumps(readback, indent=2))
    print(f"{len(replace)} replacements, {len(tasks) + len(new_tasks)} task changes, "
          f"{len(distractors)} distractors, {len(readback)} read-back questions -> {OUT}")


if __name__ == "__main__":
    main()
