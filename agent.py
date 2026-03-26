from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from .tools import read_file, write_file, run_python, install_package


# ======================
# Tool Registration
# ======================

read_tool = FunctionTool(read_file)
write_tool = FunctionTool(write_file)
run_tool = FunctionTool(run_python)
install_tool = FunctionTool(install_package)


# ======================
# 👨‍💻 Coder Agent
# ======================

coder_agent = Agent(
    model="gemini-2.5-flash",
    name="coder_agent",
    description="Responsible for creating and updating project files.",
    instruction="""
You are a professional software developer.

Responsibilities:
- Ask user for project location if not specified.
- Create new files using write_file.
- Update existing files using read_file + write_file.
- If external libraries are needed, ask for permission before installing.
- Never modify files outside the workspace.
""",
    tools=[read_tool, write_tool, install_tool]
)


# ======================
# 🧪 Debug Agent
# ======================

debug_agent = Agent(
    model="gemini-2.5-flash",
    name="debug_agent",
    description="Responsible for running and debugging Python projects.",
    instruction="""
You are a debugging specialist.

Responsibilities:
1. Run files using run_python tool.
2. If errors occur:
   - Read the file.
   - Fix the issue.
   - Rewrite the file.
   - Run again.
3. Repeat until execution succeeds.
4. Always show final execution output.
""",
    tools=[read_tool, write_tool, run_tool]
)


# ======================
# 🧠 Root Manager Agent
# ======================

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Main orchestration agent that manages development workflow.",
    instruction="""
You are the project manager.

Responsibilities:
- Understand user request.
- Ask for project location if not provided.
- Confirm before installing any packages.
- Delegate coding tasks to coder_agent.
- Delegate execution and debugging to debug_agent.
- Ensure user confirmation before modifying files outside specified folder.
- Always confirm actions taken.
""",
    sub_agents=[coder_agent, debug_agent]
)