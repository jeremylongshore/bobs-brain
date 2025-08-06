from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, CHROMA_PERSIST_DIR, SQLITE_DB_PATH
from scraper import scrape_url

# Initialize LLM (use local model)
llm = ChatOllama(model="llama3.2:latest", temperature=0)

# Initialize Chroma for RAG (using existing embeddings)
import chromadb
chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
collection = chroma_client.get_collection("bob_knowledge")

# Custom retriever for existing Chroma collection
class ChromaRetriever:
    def __init__(self, collection):
        self.collection = collection

    def invoke(self, query, config=None):
        results = self.collection.query(query_texts=[query], n_results=3)
        docs = []
        if results['documents'] and results['documents'][0]:
            from langchain_core.documents import Document
            for doc_text, metadata in zip(results['documents'][0], results['metadatas'][0] or [{}]*len(results['documents'][0])):
                docs.append(Document(page_content=doc_text, metadata=metadata))
        return docs

retriever = ChromaRetriever(collection)

# Initialize SQLite
db = SQLDatabase.from_uri(SQLITE_DB_PATH)
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = sql_toolkit.get_tools()

# Define tools
@tool
def search_chroma(query: str) -> str:
    """Search the Chroma database for relevant information."""
    try:
        docs = retriever.invoke(query)
        return "\n".join([doc.page_content for doc in docs]) or "No relevant documents found."
    except Exception as e:
        return f"Error searching Chroma: {str(e)}"

@tool
def scrape_web(url: str) -> str:
    """Scrape content from a given URL."""
    return scrape_url(url)

tools = [search_chroma, scrape_web] + sql_tools

# Define prompt for ReAct reasoning
prompt_template = PromptTemplate.from_template(
    """You are Bob, a helpful AI assistant. Use reasoning to answer user queries.

    TOOLS:
    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}"""
)

# Initialize agent with memory
memory = MemorySaver()
agent = create_react_agent(llm, tools, prompt=prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Slack integration
slack_client = WebClient(token=SLACK_BOT_TOKEN)

def handle_slack_message(event):
    try:
        user_input = event["text"]
        thread_id = event.get("thread_ts", event["ts"])
        response = agent_executor.invoke({"input": user_input})
        slack_client.chat_postMessage(
            channel=event["channel"],
            text=response["output"],
            thread_ts=thread_id
        )
    except Exception as e:
        slack_client.chat_postMessage(
            channel=event["channel"],
            text=f"Error: {str(e)}",
            thread_ts=event.get("thread_ts", event["ts"])
        )

# Slack event handler
def start_slack_bot():
    print("🔧 Starting Bob with enhanced debugging...")
    client = SocketModeClient(app_token=SLACK_APP_TOKEN)

    def process_message(client, request):
        print(f"🔍 RAW REQUEST: {request.type}")
        print(f"🔍 RAW PAYLOAD: {request.payload}")

        if request.type == "events_api":
            event = request.payload.get("event", {})
            print(f"🔍 MESSAGE EVENT - Type: {event.get('type')}, User: {event.get('user')}, Text: '{event.get('text', 'NO TEXT')}'")

            # Respond to all messages
            if event.get("type") == "message":
                print("✅ VALID MESSAGE - Processing...")
                try:
                    handle_slack_message(event)
                    print("✅ MESSAGE HANDLED")
                except Exception as e:
                    print(f"❌ ERROR HANDLING MESSAGE: {e}")
            else:
                print(f"ℹ️ Ignoring event type: {event.get('type')}")

        request.ack()

    client.socket_mode_request_listeners.append(process_message)
    print("🔌 Connecting to Slack...")
    client.connect()
    print("🤖 Bob is connected and listening for ALL events!")

    # Keep running
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("👋 Bob shutting down...")

if __name__ == "__main__":
    start_slack_bot()
