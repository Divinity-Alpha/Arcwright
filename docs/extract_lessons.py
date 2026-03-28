import json, os, glob, datetime

def extract_lessons(sessions_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    all_problems = []
    all_workarounds = []
    command_failures = {}
    command_successes = {}

    for session_file in glob.glob(os.path.join(sessions_dir, "*.json")):
        with open(session_file) as f:
            session = json.load(f)

        for problem in session.get("problems", []):
            if problem.get("resolved"):
                all_problems.append({
                    "session": session["session_name"],
                    "date": session["start_time"][:10],
                    "problem": problem["description"],
                    "root_cause": problem.get("root_cause"),
                    "resolution": problem.get("resolution"),
                    "lesson": problem.get("lesson")
                })

        for w in session.get("workarounds_needed", []):
            all_workarounds.append({
                "session": session["session_name"],
                "date": session["start_time"][:10],
                "intended": w["intended"],
                "workaround": w["workaround"],
                "why": w["why"]
            })

        for cmd in session.get("commands_used", []):
            command_successes[cmd] = command_successes.get(cmd, 0) + 1

        for failure in session.get("commands_failed", []):
            cmd = failure["command"]
            if cmd not in command_failures:
                command_failures[cmd] = []
            command_failures[cmd].append(failure["error"])

    lessons = {
        "generated": datetime.datetime.now().isoformat(),
        "total_sessions": len(glob.glob(os.path.join(sessions_dir, "*.json"))),
        "total_problems_resolved": len(all_problems),
        "total_workarounds": len(all_workarounds),
        "command_reliability": {},
        "lessons": all_problems,
        "future_commands_needed": all_workarounds,
        "unreliable_commands": []
    }

    all_commands = set(list(command_successes.keys()) + list(command_failures.keys()))
    for cmd in all_commands:
        successes = command_successes.get(cmd, 0)
        failures = len(command_failures.get(cmd, []))
        total = successes + failures
        if total > 0:
            reliability = successes / total * 100
            lessons["command_reliability"][cmd] = {
                "reliability_pct": round(reliability, 1),
                "successes": successes,
                "failures": failures,
                "common_errors": command_failures.get(cmd, [])
            }
            if reliability < 80:
                lessons["unreliable_commands"].append({
                    "command": cmd,
                    "reliability": reliability,
                    "needs_fix": True
                })

    with open(os.path.join(output_dir, "lessons.json"), "w") as f:
        json.dump(lessons, f, indent=2)

    generate_markdown(lessons, output_dir)
    print(f"Lessons extracted: {len(all_problems)} problems, {len(all_workarounds)} workarounds")
    return lessons

def generate_markdown(lessons, output_dir):
    lines = [
        "# Arcwright Knowledge Base",
        f"Generated: {lessons['generated'][:10]}",
        f"Sessions analyzed: {lessons['total_sessions']}",
        f"Problems resolved: {lessons['total_problems_resolved']}",
        "",
        "## Command Reliability",
        "| Command | Reliability | Successes | Failures |",
        "|---|---|---|---|"
    ]
    for cmd, data in sorted(lessons["command_reliability"].items(), key=lambda x: x[1]["reliability_pct"]):
        lines.append(f"| {cmd} | {data['reliability_pct']}% | {data['successes']} | {data['failures']} |")

    lines += ["", "## Lessons Learned", ""]
    for i, lesson in enumerate(lessons["lessons"], 1):
        lines += [
            f"### Lesson {i} — {lesson['problem']}",
            f"**Session:** {lesson['session']} ({lesson['date']})",
            f"**Root Cause:** {lesson['root_cause']}",
            f"**Resolution:** {lesson['resolution']}",
            f"**Lesson:** {lesson['lesson']}",
            ""
        ]

    lines += ["", "## Commands Needed (Future Arcwright Features)", ""]
    for i, w in enumerate(lessons["future_commands_needed"], 1):
        lines += [
            f"### {i}. {w['intended']}",
            f"**Workaround used:** {w['workaround']}",
            f"**Why needed:** {w['why']}",
            f"**Session:** {w['session']} ({w['date']})",
            ""
        ]

    with open(os.path.join(output_dir, "KNOWLEDGE_BASE.md"), "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    extract_lessons(
        r"C:\Arcwright\knowledge\sessions",
        r"C:\Arcwright\knowledge\reports"
    )
