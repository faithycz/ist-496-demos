from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
import gradio as gr

openai = OpenAI()

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

def chat(message, history):
    messages = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)

    while response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)

    return response.choices[0].message.content

if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        title="Digital Assistant",
        description="Talk to my personalized digital assistant who acts in place of me!",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(theme=gr.themes.Base())