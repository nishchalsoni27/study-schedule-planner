# 📚 Study Schedule Planner

A lightweight, zero-dependency Python CLI tool to **plan, log, and track** your study sessions — straight from the terminal.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Subject Management** | Add subjects with weekly hour targets and priority levels |
| **Auto Scheduler** | Generate an optimized study plan for any number of days |
| **Session Logging** | Record completed sessions with optional notes |
| **Progress Reports** | Visual ASCII progress bars per subject |
| **Goal Tracking** | Set deadlines and milestones for each subject |
| **Persistent Storage** | Data saved locally in `~/.study_planner/schedule.json` |

---

## 🚀 Quick Start

### Requirements

- Python **3.8+**
- No external libraries needed — uses the standard library only

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/study-schedule-planner.git
cd study-schedule-planner

# (Optional) Make it executable
chmod +x study_schedule_planner.py
```

---

## 🛠 Usage

### Add Subjects

```bash
python study_schedule_planner.py add-subject "Mathematics" 5 --priority 1
python study_schedule_planner.py add-subject "History" 3 --priority 2
python study_schedule_planner.py add-subject "Physics" 4
```

- `hours` = target study hours **per week**
- `--priority` = `1` (High) | `2` (Medium, default) | `3` (Low)

### List Subjects

```bash
python study_schedule_planner.py list-subjects
```

```
Subject                Hrs/Wk   Priority        Added
────────────────────────────────────────────────────────
Mathematics               5.0       HIGH   2025-04-24
Physics                   4.0        MED   2025-04-24
History                   3.0        MED   2025-04-24
```

### Generate a Schedule

```bash
# 7-day schedule, 4 study hours per day
python study_schedule_planner.py generate --days 7 --hours 4

# Custom: 5 days, 3 hours/day
python study_schedule_planner.py generate --days 5 --hours 3
```

```
📅  Study Schedule — next 7 days  (4.0h/day)
════════════════════════════════════════════════════════════

  Fri 24 Apr
    Mathematics          2.0h  ████████
    Physics              1.3h  █████
    History              0.7h  ██

  Sat 25 Apr
    Mathematics          2.0h  ████████
    ...
```

### Log a Study Session

```bash
python study_schedule_planner.py log "Mathematics" 1.5
python study_schedule_planner.py log "Physics" 2.0 --notes "Optics chapter done"
```

### View Progress Report

```bash
# Last 1 week (default)
python study_schedule_planner.py progress

# Last 2 weeks
python study_schedule_planner.py progress --weeks 2
```

```
📊  Progress — last 1 week(s)  (since 2025-04-17)
═══════════════════════════════════════════════════════
  ✅ Mathematics          4.5h /   5.0h  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░   90%
  ⚠  Physics              2.0h /   4.0h  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░   50%
  ❌ History              0.5h /   3.0h  ▓▓░░░░░░░░░░░░░░░░░░░   17%

  TOTAL    7.0h /  12.0h  (58%)
```

**Status icons:** ✅ ≥100% · ⚠️ ≥60% · ❌ <60%

### Set & View Goals

```bash
python study_schedule_planner.py set-goal "Mathematics" 2025-06-01 "Complete calculus syllabus"
python study_schedule_planner.py set-goal "Physics" 2025-05-15 "Finish optics & waves"

python study_schedule_planner.py goals
```

```
🎯  Study Goals
════════════════════════════════════════════════════════════
  📌 Mathematics          [38d left]
     Complete calculus syllabus
  📌 Physics              [21d left]
     Finish optics & waves
```

### Remove a Subject

```bash
python study_schedule_planner.py remove-subject "History"
```

### Reset All Data

```bash
python study_schedule_planner.py reset
```

---

## 📂 Project Structure

```
study-schedule-planner/
├── study_schedule_planner.py   # Main script (all-in-one)
├── README.md                   # This file
└── .gitignore                  # Standard Python gitignore
```

All data is stored at `~/.study_planner/schedule.json` and is fully portable.

---

## 🔧 Command Reference

| Command | Arguments | Options | Description |
|---|---|---|---|
| `add-subject` | `name` `hours` | `--priority 1/2/3` | Add a new subject |
| `list-subjects` | — | — | List all subjects |
| `remove-subject` | `name` | — | Delete a subject |
| `log` | `subject` `hours` | `--notes "..."` | Log a study session |
| `generate` | — | `--days N` `--hours N` | Generate schedule |
| `progress` | — | `--weeks N` | View progress report |
| `set-goal` | `subject` `date` `desc` | — | Set a study goal |
| `goals` | — | — | List all goals |
| `reset` | — | — | Clear all data |

---

## 💡 Tips

- Run `generate` at the start of each week to plan your sessions.
- Use `--priority 1` for exam subjects that need extra attention.
- Add `--notes` when logging sessions to track what you covered.
- Check `progress` daily to stay on track with your targets.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for:
- New features (e.g., Pomodoro timer, CSV export, recurring sessions)
- Bug fixes
- UI improvements

---

## 📄 License

MIT License — free to use, modify, and distribute.
