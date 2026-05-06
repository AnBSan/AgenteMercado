from typing import Literal

from langchain.messages import AIMessage, ToolMessage

from state import State
from tools import TOOLS, TOOLS_BY_NAME
from utils import load_llm, load_llm_ollama
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.constants import START, END
from langgraph.checkpoint.memory import InMemorySaver


def call_llm(state: State) -> State:
    llm = load_llm_ollama().bind_tools(TOOLS)
    result = llm.invoke(state["messages"])
    return {"messages": [result]}

def tool_node(state: State) -> State:
    llm_response = state["messages"][-1]

    if not isinstance(llm_response, AIMessage) or not getattr(
        llm_response, "tool_calls", None
    ):
        return state

    call = llm_response.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]

    try:
        content = TOOLS_BY_NAME[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError, ValueError) as error:
        content = f"Please, fix your mistakes: {error}"
        status = "error"

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)

    return {"messages": [tool_message]}

def router(state: State) -> Literal["tool_node", "__end__"]:
    llm_response = state["messages"][-1]
    
    if getattr(llm_response, "tool_calls", None):
        return "tool_node"
    return "__end__"

def build_graph() -> CompiledStateGraph[State, None, State, None]:
    builder = StateGraph(State)
    
    builder.add_node("call_llm", call_llm)
    builder.add_node("tool_node", tool_node)
    
    builder.add_edge(START, "call_llm")
    builder.add_conditional_edges("call_llm", router, ["tool_node", "__end__"])
    builder.add_edge("tool_node", "call_llm")
    
    
    return builder.compile(checkpointer=InMemorySaver())