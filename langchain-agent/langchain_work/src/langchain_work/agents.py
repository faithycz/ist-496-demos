from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_work.models import CityReport
from langchain_work.tools import get_population, get_weather
from langchain_work.middleware import log_tool_calls

def create_simple_agent():
    return create_agent(
        model="openai:gpt-5.4-mini",
        system_prompt="You are a helpful assistant who answers concisely.",
    )

def create_travel_agent():
    return create_agent(
        model="openai:gpt-5.4-mini",
        tools=[get_weather, get_population],
        system_prompt="You are a travel assistant. Use your tools to answer questions about cities.",
    )

def create_memory_agent():
    return create_agent(
        model="openai:gpt-5.4-mini",
        tools=[get_weather],
        checkpointer=MemorySaver(),
        system_prompt="You are a travel assistant. Use your tools to answer questions about cities.",
    )

def create_weather_agent():
    return create_agent(
        model="openai:gpt-5.4-mini",
        tools=[get_weather, get_population],
        response_format=CityReport,
    )

def create_watched_agent():
    return create_agent(
        model="openai:gpt-5.4-mini",
        tools=[get_weather, get_population],
        system_prompt="You are a travel assistant. Use your tools.",
        middleware=[log_tool_calls],
    )

def create_browser_agent(browser_tools):
    return create_agent(
        model="openai:gpt-5.5",
        tools=browser_tools,
        system_prompt="You are a web research assistant. Use the browser tools to complete the task, then report clearly.",
    )