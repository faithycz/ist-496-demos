from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

def get_memory():
    return MemorySaver()

def get_sqlite_memory():
    return SqliteSaver.from_conn_string("memory.db")