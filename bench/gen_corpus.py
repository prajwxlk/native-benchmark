"""Generate a deterministic synthetic startup corpus with a known decision history.

Outputs (all under data/):
  vault/                 Obsidian-style Markdown folder with [[wikilinks]] (the Markdown arm,
                         and the same folder is imported into Native for the Native arm)
  truth.json             ground truth: records, supersession chains, task->decision links
  questions.json         20 questions with answer keys
  supersedes.json        (newer_title, older_title) pairs to apply as typed links in Native
  implements.json        (task_title, decision_title) pairs

Old decisions are never edited when they are replaced, like real notes. The newer
decision says in its body which note it replaces. Meeting notes and logs mention old
values as distractors, so grepping for a value finds stale answers too.
"""
import argparse
import json
import random
import shutil
from datetime import date, timedelta
from pathlib import Path

SEED = 7
_ap = argparse.ArgumentParser()
_ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "data"))
_ap.add_argument("--scale", type=int, default=1,
                 help="multiply logs and customer calls (decisions, tasks and questions stay identical)")
ARGS = _ap.parse_args()
ROOT = Path(ARGS.out).resolve()
VAULT = ROOT / "vault" / "Fernwork HQ"
START = date(2026, 8, 3)

rng = random.Random(SEED)

PEOPLE = [
    ("Maya Okafor", "CEO and co-founder", "London"),
    ("Tom Lindqvist", "CTO and co-founder", "Stockholm"),
    ("Priya Raman", "Product designer", "Bangalore"),
    ("Daniel Reyes", "Backend engineer", "Lisbon"),
    ("Sofia Marchetti", "Growth and partnerships", "Milan"),
    ("Kenji Watanabe", "Frontend engineer", "Osaka"),
]
NAMES = [p[0] for p in PEOPLE]

ORGS = [
    ("Harbour Dental Group", "customer", "Elena Brooks", "pilot customer with 14 clinics"),
    ("Northside Physio", "customer", "Arjun Mehta", "design partner, 3 clinics"),
    ("Clearview Opticians", "customer", "Hannah Cole", "paying customer since September"),
    ("Brightpath Ventures", "investor", "Lucas Grant", "led the pre-seed round"),
    ("Kestrel Security", "vendor", "Nina Petrova", "penetration testing vendor"),
    ("Tidewater Health", "prospect", "Omar Haddad", "large hospital network prospect"),
    ("Juniper Payroll", "partner", "Grace Kim", "integration partner for staff rotas"),
    ("Atlas Cloud", "vendor", "Ben Foster", "hosting provider"),
]

# Each thread: topic, decision title stem, versions [(value, rationale)], who decides.
THREADS = [
    ("pricing", "Pricing", [
        ("£29 per clinic seat per month", "simple per-seat pricing for the pilot"),
        ("£49 per clinic per month, unlimited seats", "seat counting caused friction with Harbour Dental"),
        ("£39 per clinic per month plus £2 per booking SMS", "SMS costs were eating margin"),
    ]),
    ("launch date", "Public launch date", [
        ("15 September 2026", "aim before the autumn booking rush"),
        ("6 October 2026", "calendar sync bugs pushed the date"),
    ]),
    ("database", "Primary database", [
        ("MongoDB Atlas", "fastest to prototype with"),
        ("PostgreSQL on Atlas Cloud", "need transactions for double-booking prevention"),
    ]),
    ("target customer", "Target customer segment", [
        ("independent dental practices", "founders know the dental market"),
        ("multi-site physiotherapy and dental groups with 3 to 20 sites", "groups buy faster and churn less"),
    ]),
    ("onboarding", "Onboarding flow", [
        ("self-serve signup with a 14-day free trial", "low-touch growth"),
        ("concierge onboarding call before account creation", "trial users never imported their calendars"),
    ]),
    ("sms provider", "SMS reminder provider", [
        ("Twilio", "default choice"),
        ("MessageBird", "cheaper UK and EU rates"),
        ("Vonage", "MessageBird delivery failures in Portugal"),
    ]),
    ("mobile", "Mobile platform priority", [
        ("iOS first", "most clinic owners use iPhones"),
        ("responsive web app only, no native apps until 2027", "small team; web covers reception desks"),
    ]),
    ("support tool", "Customer support tool", [
        ("Intercom", "chat plus help centre"),
        ("Plain", "Intercom pricing jumped at 5 seats"),
    ]),
    ("analytics", "Product analytics vendor", [
        ("Mixpanel", "team familiarity"),
        ("PostHog self-hosted", "clinic data must stay in the EU"),
    ]),
    ("release cadence", "Release cadence", [
        ("weekly releases every Thursday", "predictable for pilot clinics"),
        ("continuous deploys behind feature flags", "weekly batches hid regressions"),
    ]),
    ("security audit", "Security audit vendor", [
        ("Kestrel Security", "recommended by Brightpath Ventures"),
    ]),
    ("hiring", "Next hire", [
        ("a second backend engineer", "calendar sync is the bottleneck"),
        ("a customer success lead", "concierge onboarding needs an owner"),
    ]),
    ("design system", "Design system", [
        ("Tailwind UI kit", "speed"),
    ]),
    ("investor updates", "Investor update cadence", [
        ("monthly email update on the first Monday", "Brightpath asked for monthly"),
        ("fortnightly update with a metrics dashboard link", "Brightpath wanted more frequent numbers"),
    ]),
    ("feature name", "Name of the waitlist feature", [
        ("Waitlist", "plain"),
        ("Fill-in", "clinics call it filling gaps"),
        ("Gap Filler", "Fill-in tested badly with Harbour Dental receptionists"),
    ]),
]

FILLER = [
    "Reception teams keep asking for fewer clicks when moving appointments.",
    "Calendar sync with Google and Outlook still drops edits made within the same minute.",
    "We should write up the double-booking incident properly at some point.",
    "Clinic owners care about no-show rates more than any other metric.",
    "Several receptionists asked for a dark mode on the day view.",
    "Support volume is highest on Monday mornings before 10am.",
    "The rota integration needs a clearer error when staff IDs do not match.",
    "We discussed whether SMS reminders should be sent 24 or 48 hours ahead.",
    "Exports to CSV are used weekly by clinic managers for payroll.",
    "Load testing showed the booking endpoint is fine up to 300 requests per second.",
    "Accessibility review flagged low contrast on the cancelled-appointment chips.",
    "A few clinics want per-practitioner colours on the calendar.",
]


def day(n):
    return START + timedelta(days=n)


def fm(title, **kv):
    lines = ["---", f"title: {json.dumps(title)}"]
    for k, v in kv.items():
        lines.append(f"{k}: {json.dumps(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def safe(title):
    return title.replace("/", "-").replace(":", " -").replace("?", "")


def write(folder, title, text):
    path = VAULT / folder / f"{safe(title)}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return f"{folder}/{safe(title)}.md"


def para(k=3):
    return " ".join(rng.sample(FILLER, k))


def main():
    if ROOT.joinpath("vault").exists():
        shutil.rmtree(ROOT / "vault")
    VAULT.mkdir(parents=True)
    truth = {"decisions": {}, "tasks": {}, "people": {}, "orgs": {}, "threads": {}}
    supersedes, implements = [], []

    # People
    for name, role, city in PEOPLE:
        body = fm(name, role=role) + f"# {name}\n\nRole: {role}\nBased in: {city}\n\n{para(2)}\n"
        write("Directory/People", name, body)
        truth["people"][name] = {"role": role, "city": city}

    # Orgs
    for org, kind, contact, note in ORGS:
        owner = rng.choice(["Maya Okafor", "Sofia Marchetti"])
        body = (fm(org, relationship=kind) + f"# {org}\n\nRelationship: {kind}\nMain contact: {contact}\n"
                f"Account owner: [[{owner}]]\nNotes: {note}.\n\n{para(2)}\n")
        write("Directory/Organisations", org, body)
        truth["orgs"][org] = {"kind": kind, "contact": contact, "owner": owner}

    # Decisions with supersession chains, spread over the 10 weeks
    decision_titles = {}
    for topic, stem, versions in THREADS:
        n = len(versions)
        offsets = sorted(rng.sample(range(0, 66), n))
        chain = []
        for i, ((value, why), off) in enumerate(zip(versions, offsets)):
            d = day(off)
            title = f"Decision - {stem} is {value}"
            decider = rng.choice(NAMES[:2] + [rng.choice(NAMES)])
            body = fm(title, date=d.isoformat(), status="decided", decided_by=decider)
            body += f"# {stem}: {value}\n\nDecided on {d.isoformat()} by [[{decider}]].\n\n"
            body += f"## Decision\n{stem} is **{value}**.\n\n## Why\n{why.capitalize()}.\n\n"
            if i > 0:
                prev = chain[-1]
                body += f"This replaces [[{prev}]], which is no longer current.\n\n"
                supersedes.append([title, prev])
            body += f"## Context\n{para(3)}\n"
            write("Decisions", title, body)
            chain.append(title)
            truth["decisions"][title] = {"topic": topic, "value": value, "date": d.isoformat(),
                                         "decided_by": decider, "version": i + 1, "of": n}
            decision_titles.setdefault(topic, []).append(title)
        truth["threads"][topic] = {"stem": stem, "chain": chain, "current": chain[-1],
                                   "current_value": versions[-1][0]}

    # Tasks implementing specific decision versions. Tasks for replaced decisions are
    # sometimes still open (stale work), which a good agent should notice.
    task_n = 0
    for topic, chain in decision_titles.items():
        for i, dtitle in enumerate(chain):
            for j in range(rng.choice([1, 2])):
                task_n += 1
                owner = rng.choice(NAMES)
                val = truth["decisions"][dtitle]["value"]
                verbs = ["Roll out", "Document", "Update billing and docs for", "Prepare customer comms for"]
                title = f"Task - {verbs[(task_n + j) % len(verbs)]} {truth['threads'][topic]['stem'].lower()} ({val})"
                is_current = i == len(chain) - 1
                status = rng.choice(["in_progress", "open", "completed"]) if is_current else rng.choice(["completed", "closed", "open"])
                d = day(min(69, int(truth["decisions"][dtitle]["date"][8:]) % 60 + j))
                body = fm(title, status=status, owner=owner)
                body += (f"# {title}\n\nStatus: {status}\nOwner: [[{owner}]]\nImplements: [[{dtitle}]]\n\n"
                         f"## Done when\nThe change is live for all pilot clinics and the help centre is updated.\n\n"
                         f"## Notes\n{para(2)}\n")
                write("Work/Tasks", title, body)
                truth["tasks"][title] = {"topic": topic, "decision": dtitle, "owner": owner,
                                         "status": status, "for_current": is_current}
                implements.append([title, dtitle])

    # Weekly meetings that mention decisions as they stood that week (distractors later on)
    for w in range(10):
        d = day(w * 7 + 1)
        title = f"Weekly sync {d.isoformat()}"
        lines = [fm(title, date=d.isoformat()), f"# Weekly sync, {d.isoformat()}\n",
                 "Attendees: " + ", ".join(f"[[{n}]]" for n in NAMES) + "\n"]
        for topic, chain in rng.sample(list(decision_titles.items()), 5):
            live = [t for t in chain if truth["decisions"][t]["date"] <= d.isoformat()]
            if not live:
                continue
            t = live[-1]
            lines.append(f"- {truth['threads'][topic]['stem']}: currently {truth['decisions'][t]['value']} (see [[{t}]]).")
        lines.append(f"\n## Discussion\n{para(4)}\n\n## Actions\n- {rng.choice(NAMES)} to follow up on calendar sync.\n")
        write("Meetings", title, "\n".join(lines))

    # Customer call notes
    for k in range(45 * ARGS.scale):
        org, kind, contact, _ = rng.choice(ORGS[:3] + ORGS[5:6])
        d = day(rng.randrange(0, 70))
        title = f"Call with {org} {d.isoformat()}" + (f" #{k}" if ARGS.scale > 1 else "")
        topic, chain = rng.choice(list(decision_titles.items()))
        live = [t for t in chain if truth["decisions"][t]["date"] <= d.isoformat()] or chain[:1]
        body = fm(title, date=d.isoformat()) + (
            f"# Call with {org}\n\nWith {contact}. Led by [[{rng.choice(NAMES)}]].\n\n"
            f"They asked about {truth['threads'][topic]['stem'].lower()}; we told them {truth['decisions'][live[-1]]['value']}.\n\n{para(3)}\n")
        write("Customers/Calls", title, body)

    # Daily logs: bulk that makes grep expensive, with occasional stale mentions
    for n in range(0, 70, 1):
        if day(n).weekday() >= 5:
            continue
        d = day(n)
        for who, part in [(w, p) for w in NAMES for p in range(ARGS.scale)]:
            if rng.random() > 0.65:
                continue
            title = f"Log {d.isoformat()} {who.split()[0]}" + (f" part {part + 1}" if ARGS.scale > 1 else "")
            topic, chain = rng.choice(list(decision_titles.items()))
            mention = truth["decisions"][rng.choice(chain)]["value"]
            body = fm(title, date=d.isoformat(), author=who) + (
                f"# {who.split()[0]}'s log, {d.isoformat()}\n\n## Done\n{para(4)}\n\n## Thinking\n"
                f"Thinking about {truth['threads'][topic]['stem'].lower()} ({mention}).\n{para(3)}\n\n"
                f"## Tomorrow\n{para(3)}\n")
            write(f"Logs/{d.strftime('%Y-%m')}", title, body)

    # Questions with answer keys. any_of: list of alternatives; each alternative is a list
    # of substrings that must all appear (case-insensitive).
    qs = []
    multi = [t for t in truth["threads"].values() if len(t["chain"]) >= 2]
    fresh_topics = ["pricing", "launch date", "database", "sms provider", "feature name",
                    "onboarding", "support tool", "analytics", "hiring", "investor updates"]
    for topic in fresh_topics:
        th = truth["threads"][topic]
        first = truth["decisions"][th["chain"][0]]["value"]
        qs.append({"id": f"F{len(qs)+1:02d}", "type": "freshness",
                   "question": f"Our {th['stem'].lower()} was decided as '{first}'. Is that still current? If not, what is it now?",
                   "answer": th["current_value"], "keys": key_for(th["current_value"])})
    lookups = [
        ("Who is the main contact at Harbour Dental Group?", truth["orgs"]["Harbour Dental Group"]["contact"]),
        ("What is Daniel Reyes's role?", truth["people"]["Daniel Reyes"]["role"]),
        ("Which vendor did we choose for the security audit?", "Kestrel Security"),
        ("Who is the account owner for Tidewater Health?", truth["orgs"]["Tidewater Health"]["owner"]),
        ("Where is Kenji Watanabe based?", truth["people"]["Kenji Watanabe"]["city"]),
        ("What design system did we choose?", "Tailwind UI kit"),
    ]
    for q, a in lookups:
        qs.append({"id": f"L{len(qs)-9:02d}", "type": "lookup", "question": q, "answer": a, "keys": key_for(a)})
    hops = ["pricing", "sms provider", "database", "feature name"]
    for topic in hops:
        cur = truth["threads"][topic]["current"]
        tasks = [(t, v) for t, v in truth["tasks"].items() if v["decision"] == cur]
        owners = sorted({v["owner"] for _, v in tasks})
        stem = truth["threads"][topic]["stem"].lower()
        qs.append({"id": f"M{len(qs)-15:02d}", "type": "multi_hop",
                   "question": f"Who owns the task(s) implementing our CURRENT {stem} decision? Give owner name(s).",
                   "answer": ", ".join(owners), "keys": [[o.split()[0] for o in owners]]})

    (ROOT / "truth.json").write_text(json.dumps(truth, indent=2))
    (ROOT / "questions.json").write_text(json.dumps(qs, indent=2))
    (ROOT / "supersedes.json").write_text(json.dumps(supersedes, indent=2))
    (ROOT / "implements.json").write_text(json.dumps(implements, indent=2))
    files = list(VAULT.rglob("*.md"))
    size = sum(f.stat().st_size for f in files)
    print(f"{len(files)} notes, {size/1024:.0f} KiB, {len(supersedes)} supersedes, "
          f"{len(implements)} implements, {len(qs)} questions")


def key_for(value):
    """Distinctive substrings for an answer value."""
    special = {
        "£39 per clinic per month plus £2 per booking SMS": [["39", "2"]],
        "6 October 2026": [["6 Oct"], ["2026-10-06"], ["October 6"]],
        "PostgreSQL on Atlas Cloud": [["Postgres"]],
        "concierge onboarding call before account creation": [["concierge"]],
        "fortnightly update with a metrics dashboard link": [["fortnight"], ["every two weeks"], ["biweekly"], ["bi-weekly"]],
        "a customer success lead": [["customer success"]],
        "PostHog self-hosted": [["PostHog"]],
        "Backend engineer": [["backend"]],
        "Tailwind UI kit": [["Tailwind"]],
    }
    return special.get(value, [[value]])


if __name__ == "__main__":
    main()
