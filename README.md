# Multi-Agent Coding Assistant — Google ADK + Gemini 2.5

> An autonomous coding assistant powered by **3 collaborative AI agents** that can scaffold, write, debug, and run Python projects through natural conversation — built with Google's Agent Development Kit (ADK).

---

## Demo

![Demo Screenshot](assets/demo.png)

> `coder_agent` writing files while `root_agent` manages the conversation flow

---

## How It Works

You describe what you want to build. The `root_agent` understands your request, delegates file creation to `coder_agent`, and sends the code to `debug_agent` for execution. If there are errors, `debug_agent` reads the file, fixes the bug, rewrites it, and reruns — automatically — until the code works.

```
You
 │
 ▼
root_agent  (orchestrator — understands requests, delegates work)
 ├── coder_agent
 │   ├── read_file        — reads existing files in your workspace
 │   ├── write_file       — creates and updates project files
 │   └── install_package  — pip installs (asks permission first)
 └── debug_agent
     ├── read_file        — reads code to understand errors
     ├── write_file       — rewrites fixed code
     └── run_python       — executes scripts, captures output + errors
```

| Agent | Role |
|-------|------|
| `root_agent` | Project manager — parses your intent, asks clarifying questions, delegates |
| `coder_agent` | Developer — scaffolds projects, creates and edits files |
| `debug_agent` | QA engineer — runs code, catches errors, fixes and reruns until green |

---

## Example Session

```
You:        Build a Python script that reads a CSV and prints the top 5 rows

root_agent: Where should I create the project? Please provide a folder path.

You:        /home/user/projects/csv-reader

coder_agent: [writes /home/user/projects/csv-reader/main.py]
             [asks permission to install pandas]

You:        Yes, install it

coder_agent: [installs pandas]

debug_agent: [runs main.py]
             SUCCESS:
               name  age    city
             0  Alice   30  Austin
             ...
```

---

## Security Design

All file operations are sandboxed to your workspace. The tools layer enforces this explicitly:

| Threat | Protection |
|--------|-----------|
| Path traversal (`../../../etc/passwd`) | `confirm_safe_path()` resolves absolute paths and rejects anything outside workspace root |
| Malicious package names (`; rm -rf /`) | Regex validates package names before passing to pip — letters, numbers, hyphens, underscores, dots only |
| Infinite loops / hanging scripts | `subprocess.run()` enforces a 30-second timeout |
| Accidental overwrites outside workspace | All write operations pass through the same path guard |

---

## Getting Started

**Prerequisites:** Python 3.10+, a free Google AI Studio API key

```bash
# 1. Clone the repo
git clone https://github.com/Wilson0306/adk-multi-agent-coding-assistant.git
cd adk-multi-agent-coding-assistant

# 2. Install dependencies
pip install google-adk

# 3. Add your API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 4. Launch the ADK Web UI
adk web

# 5. Open in browser
# → http://localhost:8000
```

Get a free API key at [aistudio.google.com](https://aistudio.google.com)

---

## Project Structure

```
adk-multi-agent-coding-assistant/
├── agent.py        # Agent definitions (root_agent, coder_agent, debug_agent)
├── tools.py        # File I/O, Python runner, pip installer — with security guards
├── __init__.py     # ADK entry point — exports root_agent
├── requirements.txt
├── .env.example
└── assets/
    └── demo.png
```

---

## Design Decisions

| Decision | Why |
|----------|-----|
| **3-agent split** (root/coder/debug) | Clean separation of concerns — each agent has a focused instruction set, reducing hallucination and task confusion |
| **Workspace sandboxing** | Agents should never touch files outside the user's specified folder — enforced at the tool level, not just in prompts |
| **Permission before pip install** | Installing packages is a side effect with real consequences — `root_agent` confirms with the user first |
| **Timeout on script execution** | Prevents infinite loops from hanging the entire session |
| **Gemini 2.5 Flash** | Best balance of speed and reasoning for agentic tool-use tasks at low cost |

---

## What's Next

- [ ] Add memory so agents remember past sessions and project context
- [ ] Support running full projects (`flask run`, `uvicorn`) not just single files
- [ ] Add a `planner_agent` that breaks large tasks into a structured plan before coding
- [ ] Streaming output while code runs
- [ ] Web search tool so agents can look up library docs on the fly
- [ ] VS Code extension wrapper

---

## Built With

- [Google ADK](https://google.github.io/adk-docs/) — Agent Development Kit
- [Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) — LLM backbone
- Python 3.10+

---

## Author

Built by **Wilson Tony M**
[LinkedIn](https://www.linkedin.com/in/wilson-tony-m-2335983a0) · [GitHub](https://github.com/Wilson0306)

---

## License

MIT — free to use and build on.
