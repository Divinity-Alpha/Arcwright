import json, os, glob, datetime

def generate_report(days=7):
    sessions_dir = r"C:\Arcwright\knowledge\sessions"
    reports_dir = r"C:\Arcwright\knowledge\reports"
    os.makedirs(reports_dir, exist_ok=True)

    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    recent = []

    for f in glob.glob(os.path.join(sessions_dir, "*.json")):
        with open(f) as fp:
            session = json.load(fp)
        session_date = datetime.datetime.fromisoformat(session["start_time"])
        if session_date > cutoff:
            recent.append(session)

    if not recent:
        print("No recent sessions found")
        return

    all_workarounds = []
    all_failures = []
    all_problems = []

    for session in recent:
        for p in session.get("problems", []):
            if p.get("resolved"):
                all_problems.append(p)
        for w in session.get("workarounds_needed", []):
            all_workarounds.append({**w, "session": session["session_name"]})
        for f in session.get("commands_failed", []):
            all_failures.append({**f, "session": session["session_name"]})

    lines = [
        f"# Arcwright Knowledge Report — Last {days} Days",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Sessions: {len(recent)}",
        f"Problems resolved: {len(all_problems)}",
        f"Workarounds logged: {len(all_workarounds)}",
        f"Command failures: {len(all_failures)}",
        "",
        "## Problems Resolved This Period",
        ""
    ]
    for p in all_problems:
        lines += [
            f"**Problem:** {p['description']}",
            f"**Root cause:** {p.get('root_cause', 'unknown')}",
            f"**Resolution:** {p.get('resolution', 'unknown')}",
            f"**Lesson:** {p.get('lesson', '')}",
            ""
        ]

    lines += ["## Workarounds That Need Real Commands", ""]
    for w in all_workarounds:
        lines += [
            f"**Needed:** {w['intended']}",
            f"**Used:** {w['workaround']}",
            f"**Why:** {w['why']}",
            f"**Session:** {w['session']}",
            ""
        ]

    lines += ["## Command Failures This Period", ""]
    for f in all_failures:
        lines += [f"- `{f['command']}` in {f['session']}: {f.get('error', '')}"]

    report = "\n".join(lines)
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    report_path = os.path.join(reports_dir, f"report_{date_str}.md")
    with open(report_path, "w") as f:
        f.write(report)

    print(report)
    print(f"\nSaved: {report_path}")
    print("\nPaste the above into Claude.ai for lesson analysis and CLAUDE.md updates.")

if __name__ == "__main__":
    generate_report()
