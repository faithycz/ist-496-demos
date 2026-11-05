import os
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool
from .slide_kit import build_slide

search = GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())

# set up path to sandbox for file storage and updates
def get_sandbox_path():
    sandbox = os.path.abspath("sandbox")
    os.makedirs(sandbox, exist_ok=True)
    return sandbox

@tool
def create_slide(title: str, key_points: list[str], recommendation: str) -> str:
    """Create a one-slide PowerPoint in the Voltway Research house style, saved as fleet.pptx."""

    sandbox = get_sandbox_path()

    build_slide(title, key_points, recommendation, os.path.join(sandbox, "fleet.pptx"))
    return "Saved the slide to /fleet.pptx"
