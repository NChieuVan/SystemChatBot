from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage,AIMessage
from operator import add as add_messages
from openAI import llm
from graph.prompts import system_prompt
from graph.tools import tools_dict
from services.chat_service import get_chat_memory

# Define the structure of the agent's state chat bot with AI model, for web multi users with database Pinecone
class AgentState(TypedDict):
    """
    State for each chat window per user.

    Mỗi user có thể có nhiều cửa sổ chat khác nhau.
    Mỗi cửa sổ chat tương ứng với 1 agent model + memory riêng.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    


def should_continue(state: AgentState) -> bool:
    """
    Check if last messages contain tool calls."""
    if not state.get("messages"):
        return False
    last_message = state["messages"][-1]
    return hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0

def call_llm(state: AgentState, user_id=None, chat_id=None, index_name=None) -> AgentState:
    """
        Call LLM with current state messages + memory từ Redis.
    """
    messages = list(state["messages"])
    # Lấy memory từ Redis nếu có user_id và chat_id
    if user_id and chat_id:
        memory = get_chat_memory(user_id, chat_id)
        # Chuyển memory thành list BaseMessage
        memory_msgs = []
        for m in memory:
            if m["role"] == "user":
                memory_msgs.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                memory_msgs.append(AIMessage(content=m["content"]))
        messages = memory_msgs + messages
    messages = [SystemMessage(content=system_prompt)] + messages
    response = llm.invoke(messages)
    return {"messages": [response]}

def take_action(state: AgentState) -> AgentState:
    """
    Take action based on last AI message tool calls.

    - Returns:
        Updated state with tool results appended to messages.
    """
    last_message = state["messages"][-1]
    results = []
    for tool_call in last_message.tool_calls:
        if tool_call.name in tools_dict:
            result = tools_dict[tool_call.name].invoke(tool_call.args.get("query",""), tool_call.args.get("index_name",""))
        else:
            result = f"Tool {tool_call.name} not found."
        
        results.append(ToolMessage(tool_call_id=tool_call.id, name=tool_call.name ,content=result))
    
    return {"messages": results}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever", take_action)

graph.add_conditional_edges(
    "llm", 
    should_continue,
    {True: "retriever", False: END})

graph.add_edge("retriever", "llm") 
graph.set_entry_point("llm")

agent = graph.compile()



