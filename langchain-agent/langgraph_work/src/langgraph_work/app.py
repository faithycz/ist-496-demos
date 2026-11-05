import gradio as gr
from langgraph_work.agent_memory import get_memory
from langgraph_work.agent_graph import build_graph

memory = get_memory()
graph = build_graph(checkpointer=memory)

def chat(user_input: str, history):
    config = {"configurable": {"thread_id": "gradio-session"}}
    result = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
    return f"{result['messages'][-1].content}\n\n*{result['spanish']}*"

gr.ChatInterface(chat).launch()