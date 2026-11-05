import os
from typing import Any

from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents import Agent


def llm_agent(agent_name: str, model: str, instructions: str, api_key: str = "", base_url: str = "", tools_list: list[str] | None = None) -> Agent[Any]:
    """
    This function returns an agent.

    :param agent_name: Name of agent.
    :param model: Name of model.
    :param instructions: Instructions for the agent.
    :param api_key: Name of api key. Optional for OpenAI.
    :param base_url: Name of base url. Optional for OpenAI.
    :param tools_list: Optional tool list.
    :return:
    """

    api_key_value = os.getenv(api_key)

    if base_url == "":
        """
        This is for OpenAI agents.
        """
        if tools_list is None:
            agent = Agent(name=agent_name, model=model, instructions=instructions)
        else:
            agent = Agent(name=agent_name, model=model, instructions=instructions, tools=tools_list)
    else:
        """
        This is for non-OpenAI agents (e.g. gemini).
        """
        client = AsyncOpenAI(base_url=base_url, api_key=api_key_value)
        llm_model = OpenAIChatCompletionsModel(model=model, openai_client=client)

        if tools_list is None:
            agent = Agent(name=agent_name, model=llm_model, instructions=instructions)
        else:
            agent = Agent(name=agent_name, model=llm_model, instructions=instructions, tools=tools_list)

    return agent