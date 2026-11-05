from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain.agents.middleware import TodoListMiddleware
from deepagents.middleware.filesystem import FilesystemMiddleware
from langchain_deep_agents_work.tools import search, create_slide, get_sandbox_path

def create_research_agent(model):
    sandbox = get_sandbox_path()

    backend = FilesystemBackend(root_dir=sandbox, virtual_mode=True)

    fs_middleware = FilesystemMiddleware(
        backend=backend,
        tools=["read_file", "write_file", "edit_file", "ls", "glob", "grep"],
    )

    return create_deep_agent(
        model=model,
        tools=[search],
        system_prompt=(
            "You are a research analyst. Plan your work with your todo tool, "
            "research with the search tool, and write your findings as a tidy markdown briefing to a file."
        ),
        backend=backend,
        middleware=[TodoListMiddleware(), fs_middleware],
    )

def create_vehicle_subagent():
    return {
        "name": "vehicle-researcher",
        "description": "Researches a single electric vehicle and returns a short list of facts about it.",
        "system_prompt": """You research one electric vehicle using the search tool and return three concise facts
        that a fleet buyer would care about, such as price, range and charging.
        """,
    }

def create_lead_agent(model):
    sandbox = get_sandbox_path()

    backend = FilesystemBackend(root_dir=sandbox, virtual_mode=True,)

    fs_middleware = FilesystemMiddleware(
        backend=backend,
        tools=["read_file", "write_file", "edit_file", "ls", "glob", "grep"],
    )

    return create_deep_agent(
        model=model,
        tools=[search],
        system_prompt="""
        You write comparison briefings for a company choosing electric vehicles for its sales fleet.
        For each vehicle, delegate the research to your vehicle-researcher sub-agent,
        then write a markdown comparison to a file, ending with a clear recommendation.
        """,
        subagents=[create_vehicle_subagent()],
        backend=backend,
        middleware=[TodoListMiddleware(), fs_middleware],
    )

def create_slide_maker():
    return {
        "name": "slide-maker",
        "description": "Turns a finished recommendation into a one-slide PowerPoint deck.",
        "system_prompt": "You turn research recommendations into slides, following your fleet-slide skill using the create_slide tool.",
        "tools": [create_slide],
        "skills": ["/skills/"],
    }

def create_presenter_agent(model):
    sandbox = get_sandbox_path()

    backend = FilesystemBackend(root_dir=sandbox, virtual_mode=True)

    fs_middleware = FilesystemMiddleware(
        backend=backend,
        tools=["read_file", "write_file", "edit_file", "ls", "glob", "grep"],
    )

    return create_deep_agent(
        model=model,
        subagents=[create_slide_maker()],
        system_prompt="You prepare research for presentation by delegating to your slide-maker sub-agent.",
        backend=backend,
        middleware=[TodoListMiddleware(), fs_middleware],
    )