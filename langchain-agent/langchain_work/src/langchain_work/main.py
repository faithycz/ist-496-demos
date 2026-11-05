import asyncio
from langchain_work.agents import create_browser_agent
from langchain_work.mcp import get_browser_tools
from dotenv import load_dotenv

load_dotenv(override=True)

async def main():
    browser_tools = await get_browser_tools()

    print(f"Loaded {len(browser_tools)} browser tools:")
    for t in browser_tools:
        print(" -", t.name)

    browser_agent = create_browser_agent(browser_tools)

    result = await browser_agent.ainvoke({"messages": [{"role": "user",
        "content": "Go to https://news.ycombinator.com and tell me the titles of the top three stories on the front page."}]})

    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())