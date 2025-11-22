from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage,AIMessage
from operator import add as add_messages
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from openAI import llm
from langgraph.prompts import system_prompt
from langgraph.tools import tools_dict, tools

# Define the structure of the agent's state chat bot with AI model, for web multi users with database Pinecone
class AgentState(TypedDict):
    """
    State for each chat window per user.

    Mỗi user có thể có nhiều cửa sổ chat khác nhau.
    Mỗi cửa sổ chat tương ứng với 1 agent model + memory riêng.

    Fields:
        messages: Lịch sử hội thoại (LangGraph tự merge với add_messages)
        # index_name: Pinecone index dùng để retrieve
        # user_id: ID người dùng
        # chat_id: ID cửa sổ chat (thay vì message_id)
        # last_user_message: Tin nhắn cuối cùng user gửi
        # last_ai_message: Tin nhắn cuối cùng AI trả lời
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    


def should_continue(state: AgentState) -> bool:
    """
    Check if last messages contain tool calls."""
    if not state.get("messages"):
        return False
    last_message = state["messages"][-1]
    return hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0

def call_llm(state: AgentState) -> AgentState:
    """
        Call LLM with current state messages.

        - Returns:
        AIMessage(content="...",
        tool_calls= [{"id": "tool_call_1", name": "retriever_tool", "args": { dict}}]
        }])
    """
    messages = list(state["messages"])
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



    