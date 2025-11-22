from langchain_core.tools import tool
from services.pinecone_service import retrieve_with_query


@tool()
def retriever_tool(query: str, index_name: str) -> str:
    """
    A tool to retrieve relevant documents from Pinecone indexs based on user query.
    User tool to answer question with context from Pinecone indexs.
    """
    documents = retrieve_with_query(index_name=index_name, query=query)
    if not documents:
        return "No relevant information found."
    # Combine the content of the retrieved documents into a single string
    combined_content = "\n".join([doc.page_content for doc in documents])
    return combined_content

tools = [retriever_tool]

tools_dict = {tool.name: tool for tool in tools}

