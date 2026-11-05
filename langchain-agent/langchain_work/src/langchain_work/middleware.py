from langchain.agents.middleware import wrap_tool_call

# logs tool calls that an agent makes
@wrap_tool_call
def log_tool_calls(request, handler):
    call = request.tool_call
    print(f"  [middleware] calling {call['name']} with {call['args']}")
    return handler(request)