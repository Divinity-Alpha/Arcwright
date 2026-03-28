import json, os, datetime, sys

class SessionLogger:
    def __init__(self, session_name=None):
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_name = session_name or "unnamed"
        self.log_dir = r"C:\Arcwright\knowledge\sessions"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, f"{self.session_id}_{self.session_name}.json")
        self.entries = []
        self.problems = []
        self.solutions = []
        self.commands_used = []
        self.commands_failed = []
        self.workarounds = []
        self.start_time = datetime.datetime.now().isoformat()

    def log_attempt(self, command, params, result, success):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "command",
            "command": command,
            "params": params,
            "result": result,
            "success": success
        }
        self.entries.append(entry)
        if success:
            self.commands_used.append(command)
        else:
            self.commands_failed.append({"command": command, "error": result})

    def log_problem(self, description, context, ue_error=None):
        problem = {
            "timestamp": datetime.datetime.now().isoformat(),
            "description": description,
            "context": context,
            "ue_error": ue_error,
            "resolved": False,
            "resolution": None
        }
        self.problems.append(problem)
        return len(self.problems) - 1

    def log_resolution(self, problem_index, resolution, root_cause, lesson):
        if problem_index < len(self.problems):
            self.problems[problem_index]["resolved"] = True
            self.problems[problem_index]["resolution"] = resolution
            self.problems[problem_index]["root_cause"] = root_cause
            self.problems[problem_index]["lesson"] = lesson
            self.solutions.append({
                "problem": self.problems[problem_index]["description"],
                "root_cause": root_cause,
                "resolution": resolution,
                "lesson": lesson
            })

    def log_workaround(self, intended_approach, workaround, why_needed):
        self.workarounds.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "intended": intended_approach,
            "workaround": workaround,
            "why": why_needed,
            "should_become_command": True
        })

    def save(self, summary=None):
        data = {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "start_time": self.start_time,
            "end_time": datetime.datetime.now().isoformat(),
            "summary": summary,
            "problems_encountered": len(self.problems),
            "problems_resolved": sum(1 for p in self.problems if p["resolved"]),
            "commands_used": list(set(self.commands_used)),
            "commands_failed": self.commands_failed,
            "workarounds_needed": self.workarounds,
            "problems": self.problems,
            "solutions": self.solutions,
            "entries": self.entries
        }
        with open(self.log_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Session saved: {self.log_path}")
        return self.log_path

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "unnamed"
    logger = SessionLogger(name)
    print(f"Logger initialized: {logger.log_path}")
    print("Use logger.log_attempt(), log_problem(), log_resolution(), log_workaround()")
    print("Call logger.save(summary) at end of session")
