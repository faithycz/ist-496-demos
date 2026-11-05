from dotenv import load_dotenv
from openai import OpenAI, Stream
import os

from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion import ChatCompletion

def setup(api_key: str | None = None) -> None:
    """
        This loads the environment variables and API keys.
        Checks if the given API key exists and is already loaded.

        Args:
            api_key: The API key to use.
    """
    load_dotenv("../.env", override=True)

    if api_key:
        api_key_value = os.getenv(api_key)

        if api_key_value:
            print(f"API Key exists and begins {api_key[:8]}")
        else:
            print("API Key not set - please head to the troubleshooting guide in the setup folder")

def prompt_llm(model: str, question: str, base_url = "", api_key = "") -> str | None:
    """
        Invokes and prompts an LLM and returns a response.
        If the base URL is not passed, then OpenAI is called, otherwise a specific model is called.
    """

    response = prompt_llm_raw(model, question, base_url, api_key)
    response_text = response.choices[0].message.content

    return response_text

def prompt_llm_raw(model: str, question: str, base_url = "", api_key = "") -> ChatCompletion  | Stream[ChatCompletionChunk]:
    """
        Invokes and prompts an LLM and returns a raw response showing all response details.
    """

    if base_url == "":
        client = OpenAI()
    else:
        api_key_value = os.getenv(api_key)
        client = OpenAI(base_url=base_url, api_key=api_key_value)

    messages = [{"role": "user", "content": question}]
    response = client.chat.completions.create(model=model, messages=messages)
    print(type(response))
    return response