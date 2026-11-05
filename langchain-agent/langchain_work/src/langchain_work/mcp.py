from langchain_mcp_adapters.client import MultiServerMCPClient
import sys

# for windows users
def configure_mcp_adjustment():
    if sys.platform == "win32":
        import subprocess
        from functools import partial
        import langchain_mcp_adapters.sessions as mcp_sessions

        mcp_sessions.stdio_client = partial(mcp_sessions.stdio_client, errlog=subprocess.DEVNULL)
        print("Applied the Windows adjustment")
    else:
        print("Not Windows, so nothing to do here")

def create_mcp_client():
    configure_mcp_adjustment()

    client = MultiServerMCPClient({
        "playwright": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest", "--isolated"],
        }
    })

    return client

async def get_browser_tools():
    client = create_mcp_client()
    return await client.get_tools()