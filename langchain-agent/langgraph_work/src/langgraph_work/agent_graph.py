from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph_work.agent_state import State
from langgraph_work.nodes import chatbot_node, translator_node
from langgraph_work.tools import tools

def build_graph(checkpointer=None):
    builder = StateGraph(State)

    builder.add_node("chatbot", chatbot_node)
    builder.add_node("tools", ToolNode(tools))
    builder.add_node("translator", translator_node)

    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition, {"tools": "tools", END: "translator"})
    builder.add_edge("tools", "chatbot")
    builder.add_edge("translator", END)

    return builder.compile(checkpointer=checkpointer)