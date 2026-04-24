#!/usr/bin/env python3
"""
Study Schedule Planner
A CLI tool to create, manage, and track personalized study schedules.
"""

import json
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
import argparse


DATA_FILE = Path.home() / ".study_planner" / "schedule.json"


# ─────────────────────────────────────────────
#  Data Layer
# ─────────────────────────────────────────────

def load_data() -> dict:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"subjects": {}, "sessions": [], "goals": {}}


def save_data(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


# ─────────────────────────────────────────────
#  Subject Management
# ─────────────────────────────────────────────

def add_subject(name: str, weekly_hours: float, priority: int = 2) -> None:
    """Add a new subject with a weekly hour target and priority (1=high, 2=med, 3=low)."""
    data = load_data()
    if name in data["subjects"]:
        print(f"⚠  Subject '{name}' already exists.")
        return
    data["subjects"][name] = {
        "weekly_hours": weekly_hours,
        "priority": priority,
        "color": _pick_color(len(data["subjects"])),
        "added": str(date.today()),
    }
    save_data(data)
    print(f"✅  Added subject '{name}' ({weekly_hours}h/week, priority {priority}).")


def list_subjects() -> None:
    data = load_data()
    if not data["subjects"]:
        print("No subjects yet. Use `add-subject` to get started.")
        return

    priority_label = {1: "HIGH", 2: "MED", 3: "LOW"}
    print(f"\n{'Subject':<22} {'Hrs/Wk':>7} {'Priority':>10} {'Added':>12}")
    print("─" * 56)
    for name, info in sorted(data["subjects"].items(),
                              key=lambda x: x[1]["priority"]):
        p = priority_label.get(info["priority"], str(info["priority"]))
        print(f"{name:<22} {info['weekly_hours']:>7.1f} {p:>10} {info['added']:>12}")
    print()


def remove_subject(name: str) -> None:
    data = load_data()
    if name not in data["subjects"]:
        print(f"⚠  Subject '{name}' not found.")
        return
    del data["subjects"][name]
    save_data(data)
    print(f"🗑  Removed subject '{name}'.")


# ─────────────────────────────────────────────
#  Session Logging
# ─────────────────────────────────────────────

def log_session(subject: str, hours: float, notes: str = "") -> None:
    """Log a completed study session."""
    data = load_data()
    if subject not in data["subjects"]:
        print(f"⚠  Subject '{subject}' not found. Add it first.")
        return
    session = {
        "subject": subject,
        "hours": hours,
        "date": str(date.today()),
        "notes": notes,
    }
    data["sessions"].append(session)
    save_data(data)
    print(f"📚  Logged {hours}h of '{subject}' on {date.today()}.")


# ─────────────────────────────────────────────
#  Weekly Schedule Generator
# ─────────────────────────────────────────────

def generate_schedule(days: int = 7, hours_per_day: float = 4.0) -> None:
    """Auto-generate a study plan for the next N days."""
    data = load_data()
    subjects = data["subjects"]
    if not subjects:
        print("No subjects found. Add subjects first.")
        return

    total_weekly = sum(s["weekly_hours"] for s in subjects.values())
    total_available = days * hours_per_day

    print(f"\n📅  Study Schedule — next {days} days  ({hours_per_day}h/day)")
    print("═" * 60)

    today = date.today()
    schedule = {}

    # Distribute sessions across days weighted by priority & hours
    for i in range(days):
        day = today + timedelta(days=i)
        day_label = day.strftime("%a %d %b")
        slots = []
        remaining = hours_per_day

        # Sort subjects by priority, then allocate proportionally
        sorted_subs = sorted(subjects.items(), key=lambda x: x[1]["priority"])
        for name, info in sorted_subs:
            if remaining <= 0:
                break
            ratio = info["weekly_hours"] / max(total_weekly, 0.1)
            alloc = round(min(ratio * hours_per_day, remaining, info["weekly_hours"] / 7 * 1.5), 1)
            if alloc >= 0.25:
                slots.append((name, alloc))
                remaining -= alloc

        schedule[day_label] = slots

    for day_label, slots in schedule.items():
        print(f"\n  {day_label}")
        if slots:
            for name, hrs in slots:
                bar = "█" * int(hrs * 4)
                print(f"    {name:<20} {hrs:>4.1f}h  {bar}")
        else:
            print("    (rest day)")

    scale = total_available / max(total_weekly, 0.1)
    coverage = min(scale * 100, 100)
    print(f"\n  Coverage: {coverage:.0f}% of weekly targets with {hours_per_day}h/day")
    print()


# ─────────────────────────────────────────────
#  Progress Report
# ─────────────────────────────────────────────

def progress_report(weeks: int = 1) -> None:
    """Show a summary of study hours in the last N weeks."""
    data = load_data()
    since = date.today() - timedelta(weeks=weeks)

    totals: dict[str, float] = {}
    for s in data["sessions"]:
        try:
            session_date = datetime.strptime(s["date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if session_date >= since:
            totals[s["subject"]] = totals.get(s["subject"], 0) + s["hours"]

    print(f"\n📊  Progress — last {weeks} week(s)  (since {since})")
    print("═" * 55)

    if not totals:
        print("  No sessions recorded in this period.")
        print()
        return

    subjects = data["subjects"]
    for name, logged in sorted(totals.items(), key=lambda x: -x[1]):
        target = subjects.get(name, {}).get("weekly_hours", 0) * weeks
        pct = (logged / target * 100) if target else 0
        bar_done = int(pct / 5)
        bar_todo = 20 - bar_done
        bar = "▓" * bar_done + "░" * bar_todo
        status = "✅" if pct >= 100 else ("⚠ " if pct >= 60 else "❌")
        print(f"  {status} {name:<18} {logged:>5.1f}h / {target:>5.1f}h  {bar}  {pct:>5.0f}%")

    total_logged = sum(totals.values())
    total_target = sum(
        s["weekly_hours"] * weeks for s in subjects.values()
    )
    overall = (total_logged / total_target * 100) if total_target else 0
    print(f"\n  TOTAL  {total_logged:>5.1f}h / {total_target:>5.1f}h  ({overall:.0f}%)")
    print()


# ─────────────────────────────────────────────
#  Goal Setting
# ─────────────────────────────────────────────

def set_goal(subject: str, target_date: str, description: str) -> None:
    """Set a study goal for a subject."""
    data = load_data()
    data["goals"][subject] = {
        "target_date": target_date,
        "description": description,
        "created": str(date.today()),
    }
    save_data(data)
    print(f"🎯  Goal set for '{subject}': {description} by {target_date}.")


def list_goals() -> None:
    data = load_data()
    goals = data.get("goals", {})
    if not goals:
        print("No goals set. Use `set-goal` to add one.")
        return

    print(f"\n🎯  Study Goals")
    print("═" * 60)
    today = date.today()
    for subject, g in goals.items():
        try:
            tdate = datetime.strptime(g["target_date"], "%Y-%m-%d").date()
            days_left = (tdate - today).days
            countdown = f"{days_left}d left" if days_left >= 0 else f"{-days_left}d overdue"
        except ValueError:
            countdown = g["target_date"]
        print(f"  📌 {subject:<20} [{countdown}]")
        print(f"     {g['description']}")
    print()


# ─────────────────────────────────────────────
#  Utilities
# ─────────────────────────────────────────────

def reset_data() -> None:
    if DATA_FILE.exists():
        DATA_FILE.unlink()
    print("🔄  All data cleared.")


def _pick_color(index: int) -> str:
    colors = ["cyan", "yellow", "green", "magenta", "blue", "red", "white"]
    return colors[index % len(colors)]


# ─────────────────────────────────────────────
#  CLI Entry Point
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="study-planner",
        description="📚 Study Schedule Planner — manage subjects, log sessions & track progress",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python study_schedule_planner.py add-subject "Math" 5 --priority 1
  python study_schedule_planner.py add-subject "History" 3
  python study_schedule_planner.py list-subjects
  python study_schedule_planner.py generate --days 7 --hours 4
  python study_schedule_planner.py log "Math" 1.5 --notes "Calculus chapter 3"
  python study_schedule_planner.py progress --weeks 2
  python study_schedule_planner.py set-goal "Math" 2025-06-01 "Finish calculus syllabus"
  python study_schedule_planner.py goals
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # add-subject
    p = sub.add_parser("add-subject", help="Add a new subject")
    p.add_argument("name", help="Subject name")
    p.add_argument("hours", type=float, help="Target hours per week")
    p.add_argument("--priority", type=int, choices=[1, 2, 3], default=2,
                   help="Priority: 1=high, 2=medium, 3=low (default: 2)")

    # list-subjects
    sub.add_parser("list-subjects", help="List all subjects")

    # remove-subject
    p = sub.add_parser("remove-subject", help="Remove a subject")
    p.add_argument("name", help="Subject name")

    # log
    p = sub.add_parser("log", help="Log a study session")
    p.add_argument("subject", help="Subject name")
    p.add_argument("hours", type=float, help="Hours studied")
    p.add_argument("--notes", default="", help="Optional session notes")

    # generate
    p = sub.add_parser("generate", help="Generate a study schedule")
    p.add_argument("--days", type=int, default=7, help="Number of days (default: 7)")
    p.add_argument("--hours", type=float, default=4.0,
                   help="Available study hours per day (default: 4.0)")

    # progress
    p = sub.add_parser("progress", help="Show progress report")
    p.add_argument("--weeks", type=int, default=1,
                   help="Number of past weeks to report (default: 1)")

    # set-goal
    p = sub.add_parser("set-goal", help="Set a study goal")
    p.add_argument("subject", help="Subject name")
    p.add_argument("date", help="Target date (YYYY-MM-DD)")
    p.add_argument("description", help="Goal description")

    # goals
    sub.add_parser("goals", help="List all goals")

    # reset
    sub.add_parser("reset", help="Clear all stored data")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "add-subject":    lambda: add_subject(args.name, args.hours, args.priority),
        "list-subjects":  list_subjects,
        "remove-subject": lambda: remove_subject(args.name),
        "log":            lambda: log_session(args.subject, args.hours, args.notes),
        "generate":       lambda: generate_schedule(args.days, args.hours),
        "progress":       lambda: progress_report(args.weeks),
        "set-goal":       lambda: set_goal(args.subject, args.date, args.description),
        "goals":          list_goals,
        "reset":          reset_data,
    }

    action = dispatch.get(args.command)
    if action:
        action()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
