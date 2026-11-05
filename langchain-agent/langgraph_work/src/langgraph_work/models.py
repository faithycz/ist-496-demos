from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

gpt_mini_llm = ChatOpenAI(model="gpt-5.4-mini")