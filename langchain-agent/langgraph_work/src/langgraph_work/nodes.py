from langgraph_work.models import gpt_mini_llm
from langgraph_work.tools import tools
from langgraph_work.agent_state import State

llm_with_tools = gpt_mini_llm.bind_tools(tools)

def chatbot_node(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def translator_node(state: State) -> dict:
    last = state["messages"][-1].content
    prompt = f"Translate this into Spanish, replying with the translation only:\n\n{last}"
    return {"spanish": gpt_mini_llm.invoke(prompt).content}